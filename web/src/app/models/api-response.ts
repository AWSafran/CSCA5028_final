import { Article } from "./article";
import { StockSummary } from "./stock-summary";

export interface ApiResponse {
    articles: Article[];
    stocks: StockSummary;
}