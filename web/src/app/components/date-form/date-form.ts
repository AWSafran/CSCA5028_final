import { CommonModule } from '@angular/common';
import { Component, inject, model } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { DataService } from '../../services/data-service';
import { toSignal } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-date-form',
  imports: [
    MatFormFieldModule,
    MatDatepickerModule,
    MatInputModule,
    FormsModule,
    CommonModule,
    MatCardModule,
    MatButtonModule
  ],
  providers: [provideNativeDateAdapter()],
  templateUrl: './date-form.html',
  styleUrl: './date-form.scss',
})
export class DateForm {
  dataService = inject(DataService);

  selected = model<Date | null>(null);

  error = toSignal(this.dataService.error$);
  loading = toSignal(this.dataService.loading$);

  onClick() {
    if (!this.selected()) {
      return;
    }

    const dateString = this.selected()!.toISOString().substring(0, 10);
    this.dataService.getDailySummary(dateString);
  }

}
