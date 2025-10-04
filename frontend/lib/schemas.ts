import { z } from "zod";

export const MessageSchema = z.object({
  sender: z.string(),
  message: z.string(),
  timestamp: z.string(), // Assuming it's an ISO string from JSON
});

export type Message = z.infer<typeof MessageSchema>;