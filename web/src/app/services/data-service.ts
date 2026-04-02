import { inject, Injectable } from "@angular/core";
import { ReplaySubject, take } from "rxjs";
import { StockSummary } from "../models/stock-summary";
import { Article } from "../models/article";
import { environment } from "../../environments/environment.development";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { ApiResponse } from "../models/api-response";

@Injectable({
    providedIn: 'root'
})
export class DataService {
    private httpClient = inject(HttpClient);

    stockSummary$: ReplaySubject<StockSummary | null> = new ReplaySubject<StockSummary | null>(1)
    articles$: ReplaySubject<Article[] | null> = new ReplaySubject<Article[] | null>(1)
    error$: ReplaySubject<string | null> = new ReplaySubject<string | null>(1);
    loading$: ReplaySubject<boolean> = new ReplaySubject<boolean>(1);

    getDailySummary(dateString: string) {
        this.clearData();
        const url = `${environment.apiUrl}/${dateString}`;

        this.httpClient.get<ApiResponse>(url).pipe(
            take(1)
        ).subscribe({
            next: res => this.handleSuccessResponse(res),
            error: err => this.handleErrorResponse(err)
        });
    }

    private handleSuccessResponse(response: ApiResponse) {
        this.stockSummary$.next(response.stocks);
        this.articles$.next(response.articles);
        this.loading$.next(false);
    }

    private handleErrorResponse(response: HttpErrorResponse) {
        this.error$.next(response.statusText)
        this.loading$.next(false);
    }

    private clearData() {
        this.loading$.next(true);
        this.stockSummary$.next(null);
        this.articles$.next(null);
        this.error$.next(null)
    }
    
}