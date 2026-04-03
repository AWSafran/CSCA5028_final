import { Component, computed, input } from '@angular/core';
import { Stock } from '../../models/stock';
import { MatCardModule } from '@angular/material/card';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { CurrencyPipe, DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-stock-table',
  imports: [
    MatCardModule,
    MatTableModule,
    CurrencyPipe,
    DecimalPipe
  ],
  templateUrl: './stock-table.html',
  styleUrl: './stock-table.scss',
})
export class StockTable {
  title = input.required<string>();
  stocks = input.required<Stock[]>();
  sortKey = input.required<'delta' | 'delta_pct'>();
  isDescending = input.required<boolean>();

  dataSource = computed(() => new MatTableDataSource<Stock>(this.stocks().sort(this.sortStocks)));

  readonly columns: string[] = [
    'ticker',
    'open',
    'close',
    'high',
    'delta',
    'delta_pct'
  ]

  sortStocks = (a: Stock, b: Stock): number => {
    let aVal = (this.sortKey() == 'delta' ? a.delta : a.delta_pct) ?? 0;

    let bVal = (this.sortKey() == 'delta' ? b.delta : b.delta_pct) ?? 0;

    return this.isDescending() ? bVal - aVal : aVal - bVal;
  }

  handleRowClick(row: Stock) {
    if (row.T) {
      const url = `https://www.nasdaq.com/market-activity/stocks/${row.T}`

      window.open(url, '_blank');
    }
  }
}
