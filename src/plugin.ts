import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

type EventEnvelope = {
  event?: {
    type?: string
    role?: string
    tool?: string
    input?: Record<string, unknown>
    args?: Record<string, unknown>
    message?: { role?: string }
  }
}

type PluginContext = {
  client: {
    app: {
      log: (args: {
        body: {
          service: string
          level: "debug" | "info" | "warn" | "error"
          message: string
          extra?: Record<string, unknown>
        }
      }) => Promise<unknown>
    }
  }
}

const asText = (value: unknown): string =>
  typeof value === "string" ? value : ""

const getEventType = (payload: EventEnvelope): string =>
  asText(payload?.event?.type)

const isUserMessageEvent = (payload: EventEnvelope): boolean => {
  const role =
    asText(payload?.event?.message?.role) ||
    asText(payload?.event?.role)
  return role.toLowerCase() === "user"
}

const isBashAfterEvent = (payload: EventEnvelope): boolean => {
  const type = getEventType(payload)
  if (type !== "tool.execute.after") {
    return false
  }

  const tool =
    asText(payload?.event?.tool) ||
    asText(payload?.event?.input?.tool)
  return tool.toLowerCase() === "bash"
}

const packageRoot = dirname(dirname(fileURLToPath(import.meta.url)))
const scriptPath = (name: string) => join(packageRoot, "scripts", name)

const runScript = async (pythonScript: string, payload: unknown): Promise<string> => {
  const proc = (Bun as any).spawn({
    cmd: ["python", pythonScript],
    stdin: JSON.stringify(payload),
    stdout: "pipe",
    stderr: "pipe",
    env: {
      ...process.env,
      REFLECT_RUNTIME: "opencode",
    },
  })

  const [stdoutText, stderrText] = await Promise.all([
    proc.stdout ? new Response(proc.stdout).text() : Promise.resolve(""),
    proc.stderr ? new Response(proc.stderr).text() : Promise.resolve(""),
    proc.exited,
  ])

  if (stderrText.trim()) {
    console.error(stderrText.trim())
  }
  return stdoutText.trim()
}

export const ReflectPlugin = async ({ client }: PluginContext) => {
  return {
    event: async (payload: EventEnvelope) => {
      const type = getEventType(payload)

      try {
        if (type === "session.created") {
          const out = await runScript(scriptPath("opencode_session_start_reminder.py"), payload)
          if (out) console.log(out)
          return
        }

        if (type === "experimental.session.compacting") {
          const out = await runScript(scriptPath("opencode_check_learnings.py"), payload)
          if (out) console.log(out)
          return
        }

        if ((type === "message.updated" || type === "message.part.updated") && isUserMessageEvent(payload)) {
          await runScript(scriptPath("opencode_capture_learning.py"), payload)
          return
        }

        if (isBashAfterEvent(payload)) {
          const out = await runScript(scriptPath("opencode_post_commit_reminder.py"), payload)
          if (out) console.log(out)
        }
      } catch (error) {
        await client.app.log({
          body: {
            service: "opencode-reflect",
            level: "error",
            message: "reflect plugin hook failed",
            extra: {
              eventType: type,
              error: String(error),
            },
          },
        })
      }
    },
  }
}
