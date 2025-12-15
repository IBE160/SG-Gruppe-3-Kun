import { getArticles } from "@/lib/articles";
import { Dashboard } from "@/components/Dashboard";

export default async function Home() {
  const articles = getArticles();

  return <Dashboard articles={articles} />;
}