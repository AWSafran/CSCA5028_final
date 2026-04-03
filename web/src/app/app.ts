import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { DateForm } from './components/date-form/date-form';
import { Articles } from './components/articles/articles';
import { Stocks } from './components/stocks/stocks';
@Component({
  selector: 'app-root',
  imports: [
    DateForm,
    Articles,
    Stocks
],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('web');
}
