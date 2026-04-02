import { Component, inject } from '@angular/core';
import { ArticleCard } from '../article-card/article-card';
import { DataService } from '../../services/data-service';
import { toSignal } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-articles',
  imports: [
    ArticleCard
  ],
  templateUrl: './articles.html',
  styleUrl: './articles.scss',
})
export class Articles {
  private dataService = inject(DataService)

  loading = toSignal(this.dataService.loading$)
  articles = toSignal(this.dataService.articles$)
}
