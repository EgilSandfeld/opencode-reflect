import { join } from "node:path"

type EventEnvelope = {
  type?: string
  role?: string
  tool?: string
  input?: Record<string, unknown>
  message?: { role?: string }
  part?: { role?: string }
  event?: {
    type?: string
    role?: string
    tool?: string
    input?: Record<string, unknown>
    args?: Record<string, unknown>
    message?: { role?: string }
    part?: { role?: string }
  }
}

const asText = (value: unknown): string =>
  typeof value === "string" ? value : ""

const getEventType = (payload: EventEnvelope): string =>
  asText(payload?.event?.type) || asText(payload?.type)

const isUserMessageEvent = (payload: EventEnvelope): boolean => {
  const role =
    asText(payload?.event?.message?.role) ||
    asText(payload?.event?.part?.role) ||
    asText(payload?.event?.role) ||
    asText(payload?.message?.role) ||
    asText(payload?.part?.role) ||
    asText(payload?.role)

  if (!role) {
    return true
  }

  return role.toLowerCase() === "user"
}

const isBashAfterEvent = (payload: EventEnvelope): boolean => {
  const type = getEventType(payload)
  if (type !== "tool.execute.after") {
    return false
  }

  const tool =
    asText(payload?.event?.tool) ||
    asText(payload?.event?.input?.tool) ||
    asText(payload?.tool) ||
    asText(payload?.input?.tool)
  return tool.toLowerCase() === "bash"
}

const runScript = async (scriptPath: string, payload: unknown): Promise<string> => {
  const proc = Bun.spawn({
    cmd: ["python", scriptPath],
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

export const ReflectPlugin = async ({ directory, client }) => {
  const scriptsDir = process.env.REFLECT_SCRIPTS_DIR || join(directory, "scripts")

  const script = (name: string) => join(scriptsDir, name)

  return {
    event: async (payload: EventEnvelope) => {
      const type = getEventType(payload)

      try {
        if (type === "session.created") {
          const out = await runScript(script("opencode_session_start_reminder.py"), payload)
          if (out) console.log(out)
          return
        }

        if (type === "experimental.session.compacting") {
          const out = await runScript(script("opencode_check_learnings.py"), payload)
          if (out) console.log(out)
          return
        }

        if ((type === "message.updated" || type === "message.part.updated") && isUserMessageEvent(payload)) {
          await runScript(script("opencode_capture_learning.py"), payload)
          return
        }

        if (isBashAfterEvent(payload)) {
          const out = await runScript(script("opencode_post_commit_reminder.py"), payload)
          if (out) console.log(out)
        }
      } catch (error) {
        await client.app.log({
          body: {
            service: "reflect-plugin",
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
