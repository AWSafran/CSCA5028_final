import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StockTable } from './stock-table';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { StockSummary } from '../../models/stock-summary';
import { Stock } from '../../models/stock';

describe('StockTable', () => {
  let component: StockTable;
  let fixture: ComponentFixture<StockTable>;

  let mockStocks: Stock[] = [
    {
      T: 'NOM_MAX',
      _id: {
        $oid: '69c5bafec41f9585496ac273'
      },
      c: 801.99,
      delta: 999,
      delta_pct: 0.100349866227619,
      fetch_date: '2026-03-24',
      h: 803.58,
      l: 728.85,
      n: 189872,
      o: 728.85,
      t: 1774382400000,
      v: 6993697.97582,
      vw: 781.2247
    },
    {
      T: 'NOM_MIN',
      _id: {
        $oid: '69c5bafec41f9585496ac273'
      },
      c: 801.99,
      delta: -999,
      delta_pct: 0.100349866227619,
      fetch_date: '2026-03-24',
      h: 803.58,
      l: 728.85,
      n: 189872,
      o: 728.85,
      t: 1774382400000,
      v: 6993697.97582,
      vw: 781.2247
    },
    {
      T: 'PCT_MAX',
      _id: {
        $oid: '69c5bafec41f9585496ac273'
      },
      c: 801.99,
      delta: 10,
      delta_pct: 1,
      fetch_date: '2026-03-24',
      h: 803.58,
      l: 728.85,
      n: 189872,
      o: 728.85,
      t: 1774382400000,
      v: 6993697.97582,
      vw: 781.2247
    },
    {
      T: 'PCT_MIN',
      _id: {
        $oid: '69c5bafec41f9585496ac273'
      },
      c: 801.99,
      delta: 100,
      delta_pct: -1,
      fetch_date: '2026-03-24',
      h: 803.58,
      l: 728.85,
      n: 189872,
      o: 728.85,
      t: 1774382400000,
      v: 6993697.97582,
      vw: 781.2247
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StockTable],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StockTable);
    component = fixture.componentInstance;
    fixture.componentRef.setInput('title', 'testTitle');
    fixture.componentRef.setInput('stocks', mockStocks);
    fixture.componentRef.setInput('sortKey', 'delta')
    fixture.componentRef.setInput('isDescending', true);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should sort', () => {
    expect(component.dataSource().data[0].T).toEqual('NOM_MAX');

    fixture.componentRef.setInput('isDescending', false);
    expect(component.dataSource().data[0].T).toEqual('NOM_MIN');

    fixture.componentRef.setInput('sortKey', 'delta_pct')
    expect(component.dataSource().data[0].T).toEqual('PCT_MIN');

    fixture.componentRef.setInput('isDescending', true)
    expect(component.dataSource().data[0].T).toEqual('PCT_MAX');
  });

  it('should render title', () => {
    const matCardTitle = fixture.nativeElement.querySelector('mat-card-title');
    expect(matCardTitle.textContent).toContain(component.title());
  });

  it('should react to row clicks', () => {
    const dataRow = fixture.debugElement.nativeElement.querySelector('td');
    spyOn(component, 'handleRowClick');
    dataRow.click();
    expect(component.handleRowClick).toHaveBeenCalled();
  });
});
