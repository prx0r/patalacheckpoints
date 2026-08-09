export const metadata = {
  title: "Śaiva Tantra Atlas",
  description: "A research workstation for medieval Śaiva texts — traditions, texts, people, and concepts in a navigable graph.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
