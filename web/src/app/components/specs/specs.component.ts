import { Component, OnInit } from '@angular/core';

import { PackageService } from '../../services/package/package.service';

@Component({
  selector: 'app-specs',
  templateUrl: './specs.component.html',
  styleUrls: ['./specs.component.css'],
})
export class SpecsComponent implements OnInit {
  constructor(public packageService: PackageService) {}

  ngOnInit(): void {
    this.packageService.specsComponentOnInit();
  }
}
