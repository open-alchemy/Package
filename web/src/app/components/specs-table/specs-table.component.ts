import { Component, Input } from '@angular/core';

import { SpecInfo } from '../../services/package/package.reducer';

@Component({
  selector: 'app-specs-table',
  templateUrl: './specs-table.component.html',
  styleUrls: ['./specs-table.component.css'],
})
export class SpecsTableComponent {
  displayedColumns: string[] = [
    'id',
    'title',
    'description',
    'version',
    'updated_at',
    'model_count',
  ];
  @Input() specInfos: SpecInfo[] = [];

  constructor() {}
}
