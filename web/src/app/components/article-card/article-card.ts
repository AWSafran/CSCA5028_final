import { Component, computed, input, Input } from '@angular/core';
import { Article } from '../../models/article';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-article-card',
  imports: [
    MatCardModule
  ],
  templateUrl: './article-card.html',
  styleUrl: './article-card.scss',
})
export class ArticleCard {
  article = input.required<Article>();

  title = computed(() => this.article().title);
  imageUrl = computed(() => this.article().urlToImage);
  date = computed(() => this.article().fetch_date);
  sourceName = computed(() => this.article().source?.name);
  author = computed(() => this.article().author);
  url = computed(() => this.article().url);
  description = computed(() => this.article().description);
}
