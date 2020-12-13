import { Component, Input } from '@angular/core';

import { PackageService } from '../../services/package/package.service';
import { SpecId } from '../../services/package/types';

@Component({
  selector: 'app-specs-manage-spec',
  templateUrl: './specs-manage-spec.component.html',
  styleUrls: ['./specs-manage-spec.component.css'],
})
export class SpecsManageSpecComponent {
  @Input() specId: SpecId | null = null;
  deleteDisabled = false;

  constructor(private packageService: PackageService) {}

  deleteButtonClick(): void {
    if (this.specId !== null) {
      this.packageService.specsComponentDeleteSpec(this.specId);
      this.deleteDisabled = true;
    }
  }
}
