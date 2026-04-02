import { CommonModule } from '@angular/common';
import { Component, model } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

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
  selected = model<Date | null>(null);

  

}
