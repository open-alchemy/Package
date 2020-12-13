import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-specs-refresh-button',
  templateUrl: './specs-refresh-button.component.html',
  styleUrls: ['./specs-refresh-button.component.css'],
})
export class SpecsRefreshButtonComponent {
  @Input() loading = true;
  @Output() refreshEvent = new EventEmitter<void>();

  refresh(): void {
    this.refreshEvent.emit();
  }
}
