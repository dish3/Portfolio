import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NOVA — AI-Managed Personal Portfolio OS",
  description: "An autonomous AI portfolio operating system with story-driven public presentation and intelligent ingestion.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground antialiased selection:bg-accent-amber/30 selection:text-foreground">
        {children}
      </body>
    </html>
  );
}
