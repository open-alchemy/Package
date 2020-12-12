export function decodeResponse(value: string): string {
  try {
    return atob(value);
  } catch {
    return JSON.stringify(value);
  }
}
