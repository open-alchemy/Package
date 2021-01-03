import { Component, OnInit, Input } from '@angular/core';

import { PackageService } from '../../services/package/package.service';
import { SpecId, Credentials, SpecVersion } from '../../services/package/types';

@Component({
  selector: 'app-credentials',
  templateUrl: './credentials.component.html',
  styleUrls: ['./credentials.component.css'],
})
export class CredentialsComponent implements OnInit {
  @Input() specId: SpecId | null = null;
  @Input() specVersion: SpecVersion | null = null;

  constructor(public packageService: PackageService) {}

  ngOnInit(): void {}

  calculatePipInstall(
    credentials: Credentials,
    specId: SpecId,
    version: SpecVersion
  ): string {
    return (
      `pip install -f https://${credentials.public_key}:${credentials.secret_key}` +
      `@index.package.openalchemy.io "${specId}==${version}"`
    );
  }
}
