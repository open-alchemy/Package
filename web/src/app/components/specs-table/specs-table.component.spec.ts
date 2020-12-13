import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DatePipe } from '@angular/common';

import { MatTableModule } from '@angular/material/table';

import { SpecInfo } from '../../services/package/types';
import { SpecsTableComponent } from './specs-table.component';

const SPEC_INFO_1: SpecInfo = {
  spec_id: 'spec id 1',
  version: 'version 1',
  model_count: 1,
};
const SPEC_INFO_2: SpecInfo = {
  spec_id: 'spec id 2',
  version: 'version 2',
  title: 'title 2',
  description: 'description 2',
  updated_at: 2000000,
  model_count: 2,
};

describe('SpecsTableComponent', () => {
  let component: SpecsTableComponent;
  let fixture: ComponentFixture<SpecsTableComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SpecsTableComponent],
      imports: [MatTableModule],
    });

    fixture = TestBed.createComponent(SpecsTableComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should only show headers if there are no specs', () => {
    // GIVEN

    // WHEN detectChanges is called
    fixture.detectChanges();

    // THEN a table with headers only is defined
    const table: HTMLTableElement = fixture.nativeElement.querySelector(
      'table'
    );
    expect(table).toBeTruthy();
    const trs = table.querySelectorAll('tr');
    expect(trs.length).toEqual(1);
    const ths = trs[0].querySelectorAll('th');
    expect(ths.length).toEqual(component.displayedColumns.length);
  });

  it('should only show a single row with optional values not shown if a single spec is provided without optional values', () => {
    // GIVEN component with some values defined
    component.specInfos = [SPEC_INFO_1];

    // WHEN detectChanges is called
    fixture.detectChanges();

    // THEN a table with headers only is defined
    const table: HTMLTableElement = fixture.nativeElement.querySelector(
      'table'
    );
    expect(table).toBeTruthy();
    const trs = table.querySelectorAll('tr');
    expect(trs.length).toEqual(2);
    const tds = trs[1].querySelectorAll('td');
    expect(tds.length).toEqual(component.displayedColumns.length);
    const tdInnerTexts = new Set(Array.from(tds).map((td) => td.innerText));
    expect(tdInnerTexts).toContain(SPEC_INFO_1.spec_id);
    expect(tdInnerTexts).toContain(SPEC_INFO_1.version);
    expect(tdInnerTexts).toContain(SPEC_INFO_1.model_count.toString());
  });

  it('should only show a single row with optional values shown if a single spec is provided with optional values', () => {
    // GIVEN component with some values defined
    component.specInfos = [SPEC_INFO_2];

    // WHEN detectChanges is called
    fixture.detectChanges();

    // THEN a table with headers only is defined
    const table: HTMLTableElement = fixture.nativeElement.querySelector(
      'table'
    );
    expect(table).toBeTruthy();
    const trs = table.querySelectorAll('tr');
    expect(trs.length).toEqual(2);
    const tds = trs[1].querySelectorAll('td');
    expect(tds.length).toEqual(component.displayedColumns.length);
    const tdInnerTexts = new Set(Array.from(tds).map((td) => td.innerText));
    expect(tdInnerTexts).toContain(SPEC_INFO_2.spec_id);
    expect(tdInnerTexts).toContain(SPEC_INFO_2.version);
    expect(tdInnerTexts).toContain(SPEC_INFO_2.title);
    expect(tdInnerTexts).toContain(SPEC_INFO_2.description);
    expect(tdInnerTexts).toContain(
      new DatePipe('en').transform(
        (SPEC_INFO_2.updated_at ? SPEC_INFO_2.updated_at : 0) * 1000,
        'medium'
      )
    );
    expect(tdInnerTexts).toContain(SPEC_INFO_2.model_count.toString());
  });

  it('should only show a multiple rows if multiple specs are provided', () => {
    // GIVEN component with some values defined
    component.specInfos = [SPEC_INFO_1, SPEC_INFO_2];

    // WHEN detectChanges is called
    fixture.detectChanges();

    // THEN a table with headers only is defined
    const table: HTMLTableElement = fixture.nativeElement.querySelector(
      'table'
    );
    expect(table).toBeTruthy();
    const trs = table.querySelectorAll('tr');
    expect(trs.length).toEqual(3);
    let tds = trs[1].querySelectorAll('td');
    expect(tds.length).toEqual(component.displayedColumns.length);
    tds = trs[2].querySelectorAll('td');
    expect(tds.length).toEqual(component.displayedColumns.length);
  });
});
