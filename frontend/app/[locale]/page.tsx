import { getArticles } from "@/lib/articles";
import { Dashboard } from "@/components/Dashboard";

export default async function Home({
  params
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const articles = getArticles(locale);

  return <Dashboard articles={articles} />;
}