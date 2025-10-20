import { apiRequest } from "./index.api";

export async function getRules(gameType: string): Promise<string> {
    return apiRequest<string>(`/docs/rules/${gameType}`, {
        method: "GET",
    });
}
