import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DateForm } from './date-form';

describe('DateForm', () => {
  let component: DateForm;
  let fixture: ComponentFixture<DateForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DateForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DateForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
