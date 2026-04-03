import { Component, inject } from '@angular/core';
import { StockTable } from '../stock-table/stock-table';
import { DataService } from '../../services/data-service';
import { toSignal } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-stocks',
  imports: [StockTable],
  templateUrl: './stocks.html',
  styleUrl: './stocks.scss',
})
export class Stocks {
  private dataService = inject(DataService);

  stockSummary = toSignal(this.dataService.stockSummary$);
  loading = toSignal(this.dataService.loading$);
}
