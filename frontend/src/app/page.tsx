import { apiFetch } from "@/lib/api";

interface HealthResponse {
  status: string;
}

async function getApiHealth(): Promise<HealthResponse | null> {
  try {
    return await apiFetch<HealthResponse>("/api/health");
  } catch {
    return null;
  }
}

export default async function Home() {
  const health = await getApiHealth();

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-950">
      <main className="flex w-full max-w-2xl flex-col gap-10 rounded-2xl bg-white p-12 shadow-sm dark:bg-zinc-900">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            VisaApp
          </h1>
          <p className="mt-2 text-zinc-500 dark:text-zinc-400">
            FastAPI + Next.js boilerplate
          </p>
        </div>

        <div className="rounded-xl border border-zinc-200 p-6 dark:border-zinc-700">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-widest text-zinc-400">
            Backend Health
          </h2>
          {health ? (
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-green-500" />
              <span className="font-medium text-green-600 dark:text-green-400">
                API is reachable — status: {health.status}
              </span>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-red-400" />
              <span className="text-red-500 dark:text-red-400">
                Could not reach the API. Make sure the backend is running on{" "}
                <code className="rounded bg-zinc-100 px-1 dark:bg-zinc-800">
                  {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}
                </code>
                .
              </span>
            </div>
          )}
        </div>

        <div className="space-y-2 text-sm text-zinc-500 dark:text-zinc-400">
          <p>
            Backend docs:{" "}
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium text-zinc-900 underline-offset-2 hover:underline dark:text-zinc-100"
            >
              localhost:8000/docs
            </a>
          </p>
          <p>
            Frontend:{" "}
            <a
              href="http://localhost:3000"
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium text-zinc-900 underline-offset-2 hover:underline dark:text-zinc-100"
            >
              localhost:3000
            </a>
          </p>
        </div>
      </main>
    </div>
  );
}
