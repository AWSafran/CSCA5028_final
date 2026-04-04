import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Articles } from './articles';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { Article } from '../../models/article';
import { DataService } from '../../services/data-service';

describe('Articles', () => {
  let component: Articles;
  let fixture: ComponentFixture<Articles>;
  let dataService: DataService;

  let mockArticles: Article[] = [
    {
      _id: {
        $oid: "69c5bafec41f9585496abf95"
      },
      author: "Seth Borenstein",
      content: "After smashing March heat records in 14 states and the U.S. as a whole, the gigantic heat dome thats baked the Southwest is creeping eastward and may end up being one of the most expansive heat waves… [+4219 chars]",
      description: "A huge heat dome is spreading across the United States and it is shattering March temperature records. On Monday, National Weather Service meteorologist Gregg Gallina said the heat covers an unusually large area. Weather historians say the dome has already sm…",
      fetch_date: "2026-03-24",
      publishedAt: "2026-03-24T12:07:36Z",
      source: {
        id: "associated-press",
        name: "Associated Press"
      },
      title: "Record-smashing heat spreads: 'Basically the entire nation is going to be hot'...",
      url: "https://apnews.com/article/record-heat-climate-warming-arizona-california-11dcebf8ba88cfcd3fd9bc1144a5df10",
      urlToImage: "https://dims.apnews.com/dims4/default/d7b678c/2147483647/strip/true/crop/2000x1333+0+0/resize/980x653!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2Fd8%2F2c%2F142d404b3135ed41a907b8facf0a%2Fc3b1018a0c3d486f8a135addfcacc1cc"
    },
    {
      _id: {
        $oid: "69c5bafec41f9585496abf96"
      },
      author: "Aamer Madhani",
      content: "WASHINGTON (AP) President Donald Trump started the fourth week of his war against Iran by offering the world some guarded optimism that the U.S. could soon be winding operations down, a claim that ma… [+6429 chars]",
      description: "President Donald Trump started the fourth week of his war against Iran by offering the world some guarded optimism that the U.S. could soon be winding down its military operations. It was a claim that buoyed markets on Monday. But Iranian officials dismissed …",
      fetch_date: "2026-03-24",
      publishedAt: "2026-03-24T10:37:36Z",
      source: {
        id: "associated-press",
        name: "Associated Press"
      },
      title: "DE-ESCALATION SKEPTICISM",
      url: "https://apnews.com/article/trump-iran-talks-objectives-e27ba37004edf6dc241417ad11c87760",
      urlToImage: "https://dims.apnews.com/dims4/default/5419a28/2147483647/strip/true/crop/4592x3060+0+1/resize/980x653!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2Fd1%2F9a%2F9921ecf048eed7347c2e8e9687fa%2F2b8bff7590bb4a24812580b640c6eed9"
    },
    {
      _id: {
        $oid: "69c5bafec41f9585496abf97"
      },
      author: "CBS News",
      content: "Copyright ©2026 CBS Interactive Inc. All rights reserved.",
      description: "A recent CBS News poll shows how Americans feel about the U.S. involvement in the Iran war. CBS News' Anthony Salvanto has the data.",
      fetch_date: "2026-03-24",
      publishedAt: "2026-03-24T13:10:00Z",
      source: {
        id: "cbs-news",
        name: "CBS News"
      },
      title: "New poll shows most Americans are against U.S. involvement in Iran war",
      url: "https://www.cbsnews.com/video/new-poll-shows-most-americans-are-against-us-involvement-in-iran-war/",
      urlToImage: "https://assets3.cbsnewsstatic.com/hub/i/r/2026/03/24/b45269c6-49e5-4f3c-8705-4e40c8b33a79/thumbnail/1200x630/6b9412a448a30c685642d5f4548a0b6e/cbsn-fusion-new-poll-shows-most-americans-are-against-us-involvement-in-iran-war-thumbnail.jpg"
    }
  ]

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Articles],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Articles);
    component = fixture.componentInstance;
    dataService = TestBed.inject(DataService);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display article card components', () => {
    dataService.articles$.next(mockArticles);

    fixture.detectChanges();

    const articleCards = fixture.nativeElement.querySelectorAll('app-article-card');
    expect(articleCards.length).toEqual(mockArticles.length)
  })
});
