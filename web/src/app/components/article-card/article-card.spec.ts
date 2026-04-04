import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleCard } from './article-card';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { Article } from '../../models/article';

describe('ArticleCard', () => {
  let component: ArticleCard;
  let fixture: ComponentFixture<ArticleCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ArticleCard],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ArticleCard);
    let testArticle: Article = {
        _id: {
          $oid: "oid"
        },
        source: {
          id: "sourceId",
          name: "SourceName"
        },
        author: 'author',
        title: 'title',
        description: 'desc',
        url: 'https://url',
        urlToImage: 'https://imageUrl',
        publishedAt: 'publishDate',
        content: 'content',
        fetch_date: '2026-03-24',
    }
    component = fixture.componentInstance;
    fixture.componentRef.setInput('article', testArticle);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display card', () => {
    expect(fixture.nativeElement.querySelector('mat-card')).toBeTruthy();
  });

  it('should link to article', () => {
    let anchor = fixture.nativeElement.querySelector('a')
    expect(anchor.href).toEqual('https://url/')
  });

  it('should display title', () => {
    let title = fixture.nativeElement.querySelector('mat-card-title')
    expect(title.innerText).toEqual('title')
  });

  it('should display subtitle', () => {
    let subtitle = fixture.nativeElement.querySelector('mat-card-subtitle')
    expect(subtitle.innerText).toEqual('author - SourceName')
  });

  it('should display description', () => {
    let content = fixture.nativeElement.querySelector('mat-card-content')
    expect(content.innerText).toEqual('desc')
  });

  it('should display date', () => {
    let footer = fixture.nativeElement.querySelector('mat-card-footer')
    expect(footer.innerText).toEqual('2026-03-24')
  });

  it('should display image', () => {
    let image = fixture.nativeElement.querySelector('img')
    expect(image.src).toEqual('https://imageurl/')
  });

});
