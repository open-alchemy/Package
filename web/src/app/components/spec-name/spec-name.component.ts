import { Component, Input } from '@angular/core';

import { SpecInfo } from '../../services/package/package.reducer';

@Component({
  selector: 'app-spec-name',
  templateUrl: './spec-name.component.html',
  styleUrls: ['./spec-name.component.css'],
})
export class SpecNameComponent {
  @Input() specInfo: SpecInfo | null = null;
}
