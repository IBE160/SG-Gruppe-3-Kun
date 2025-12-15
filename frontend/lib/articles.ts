import fs from 'fs';
import path from 'path';

export interface Article {
  slug: string;
  title: string;
  content: string;
}

const articlesDirectory = path.join(process.cwd(), 'data/articles');

export function getArticles(): Article[] {
  // Create directory if it doesn't exist to avoid errors
  if (!fs.existsSync(articlesDirectory)) {
    return [];
  }

  const fileNames = fs.readdirSync(articlesDirectory);
  const articles = fileNames
    .filter((fileName) => fileName.endsWith('.md'))
    .map((fileName) => {
      const slug = fileName.replace(/\.md$/, '');
      const fullPath = path.join(articlesDirectory, fileName);
      const fileContents = fs.readFileSync(fullPath, 'utf8');

      // Simple title extraction (first line starting with #)
      const titleMatch = fileContents.match(/^#\s+(.+)$/m);
      const title = titleMatch ? titleMatch[1] : slug;

      return {
        slug,
        title,
        content: fileContents,
      };
    });

  return articles;
}

export function getArticle(slug: string): Article | null {
  try {
    const fullPath = path.join(articlesDirectory, `${slug}.md`);
    if (!fs.existsSync(fullPath)) {
      return null;
    }
    
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const titleMatch = fileContents.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1] : slug;

    return {
      slug,
      title,
      content: fileContents,
    };
  } catch (error) {
    return null;
  }
}
