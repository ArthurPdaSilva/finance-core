import { describe, expect, it } from "vitest";
import { fakeChats } from "./fake-chat";

describe("fakeChats", () => {
  it("contains unique ids and titles for the local menu fixture", () => {
    const ids = fakeChats.map((chat) => chat.id);

    expect(fakeChats).not.toHaveLength(0);
    expect(new Set(ids).size).toBe(ids.length);
    expect(fakeChats.every((chat) => chat.title.length > 0)).toBe(true);
  });
});
