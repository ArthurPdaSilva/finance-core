import { describe, expect, it, vi } from "vitest";
import { asyncDelay } from "./async-delay";

describe("asyncDelay", () => {
  it("resolves immediately for non-positive durations", async () => {
    await expect(asyncDelay(0)).resolves.toBeUndefined();
  });

  it("waits for a positive duration", async () => {
    vi.useFakeTimers();
    const promise = asyncDelay(100);

    await vi.advanceTimersByTimeAsync(100);

    await expect(promise).resolves.toBeUndefined();
    vi.useRealTimers();
  });
});
