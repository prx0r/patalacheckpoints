export const metadata = {
  title: "Pāṭala — Tantra Hub",
  description: "The authority, provenance, and expert-validation layer for tantric textual heritage. Read translations where every interpretive decision is inspectable.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <head />
      <body className="antialiased">{children}</body>
    </html>
  );
}
