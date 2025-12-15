import fs from 'fs';
import path from 'path';

export interface Article {
  slug: string;
  title: string;
  content: string;
}

const articlesDirectory = path.join(process.cwd(), 'data/articles');

export function getArticles(locale: string = 'en'): Article[] {
  // Use locale-specific subdirectory, fallback to 'en' if 'no' is empty or on error?
  // Actually, let's just look in the specific locale folder.
  const localeDirectory = path.join(articlesDirectory, locale);

  // Create directory if it doesn't exist to avoid errors
  if (!fs.existsSync(localeDirectory)) {
    return [];
  }

  const fileNames = fs.readdirSync(localeDirectory);
  const articles = fileNames
    .filter((fileName) => fileName.endsWith('.md'))
    .map((fileName) => {
      const slug = fileName.replace(/\.md$/, '');
      const fullPath = path.join(localeDirectory, fileName);
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

export function getArticle(slug: string, locale: string = 'en'): Article | null {
  try {
    const fullPath = path.join(articlesDirectory, locale, `${slug}.md`);
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
