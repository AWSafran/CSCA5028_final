import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { DateForm } from './components/date-form/date-form';

@Component({
  selector: 'app-root',
  imports: [
    DateForm
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('web');
}
