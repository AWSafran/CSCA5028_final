import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';

import { DateForm } from './date-form';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { SelectionModel } from '@angular/cdk/collections';
import { By } from '@angular/platform-browser';
import { DataService } from '../../services/data-service';

describe('DateForm', () => {
  let component: DateForm;
  let fixture: ComponentFixture<DateForm>;
  let dataService: DataService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DateForm],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DateForm);
    dataService = TestBed.inject(DataService)
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call data service search method', fakeAsync(() => {
    component.selected.set(new Date('2026-03-24'));

    spyOn(dataService, 'getDailySummary')

    fixture.detectChanges();

    component.onClick();
    
    expect(dataService.getDailySummary).toHaveBeenCalledOnceWith('2026-03-24')
    
  }));
});
