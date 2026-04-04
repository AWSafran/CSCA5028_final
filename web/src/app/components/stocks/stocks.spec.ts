import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Stocks } from './stocks';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { StockSummary } from '../../models/stock-summary';
import { DataService } from '../../services/data-service';

describe('Stocks', () => {
  let component: Stocks;
  let fixture: ComponentFixture<Stocks>;
  let dataService: DataService;

  let mockStockSummary: StockSummary = {
    nominal_max: [
      {
        T: "LITE",
        _id: {
          $oid: "69c5bafec41f9585496ac273"
        },
        c: 801.99,
        delta: 73.14,
        delta_pct: 0.100349866227619,
        fetch_date: "2026-03-24",
        h: 803.58,
        l: 728.85,
        n: 189872,
        o: 728.85,
        t: 1774382400000,
        v: 6993697.97582,
        vw: 781.2247
      }
    ],
    nominal_min: [
      {
        T: "LITE",
        _id: {
          $oid: "69c5bafec41f9585496ac273"
        },
        c: 801.99,
        delta: 73.14,
        delta_pct: 0.100349866227619,
        fetch_date: "2026-03-24",
        h: 803.58,
        l: 728.85,
        n: 189872,
        o: 728.85,
        t: 1774382400000,
        v: 6993697.97582,
        vw: 781.2247
      }
    ],
    percent_max: [
      {
        T: "LITE",
        _id: {
          $oid: "69c5bafec41f9585496ac273"
        },
        c: 801.99,
        delta: 73.14,
        delta_pct: 0.100349866227619,
        fetch_date: "2026-03-24",
        h: 803.58,
        l: 728.85,
        n: 189872,
        o: 728.85,
        t: 1774382400000,
        v: 6993697.97582,
        vw: 781.2247
      }
    ],
    percent_min: [
      {
        T: "LITE",
        _id: {
          $oid: "69c5bafec41f9585496ac273"
        },
        c: 801.99,
        delta: 73.14,
        delta_pct: 0.100349866227619,
        fetch_date: "2026-03-24",
        h: 803.58,
        l: 728.85,
        n: 189872,
        o: 728.85,
        t: 1774382400000,
        v: 6993697.97582,
        vw: 781.2247
      }
    ]
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Stocks],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Stocks);
    component = fixture.componentInstance;
    dataService = TestBed.inject(DataService);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display stocktable components', () => {
    dataService.stockSummary$.next(mockStockSummary);

    fixture.detectChanges();

    const stockTables = fixture.nativeElement.querySelectorAll('app-stock-table')
    expect(stockTables.length).toEqual(4);
  });
});
