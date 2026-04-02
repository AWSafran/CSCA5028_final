import { ArticleSource } from "./article-source";
import { ObjectId } from "./object-id";

export interface Article {
    _id: ObjectId;
    source?: ArticleSource;
    author?: string;
    title?: string;
    description?: string;
    url?: string;
    urlToImage?: string;
    publishedAt?: string;
    content?: string;
    fetch_date?: string;
}