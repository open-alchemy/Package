import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpecInfo } from '../../services/package/package.reducer';

import { SpecNameComponent } from './spec-name.component';

describe('SpecNameComponent', () => {
  let component: SpecNameComponent;
  let fixture: ComponentFixture<SpecNameComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SpecNameComponent],
    });

    fixture = TestBed.createComponent(SpecNameComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should not display anything if specInfo is None', () => {
    // GIVEN

    // WHEN changes are detected
    fixture.detectChanges();

    // THEN no paragraph elements are shown
    const ps: NodeListOf<HTMLParagraphElement> = fixture.nativeElement.querySelectorAll(
      'p'
    );
    expect(ps.length).toEqual(0);
  });

  it('should display name and id if the specInfo is set', () => {
    // GIVEN component with specInfo set
    const specInfo: SpecInfo = {
      name: 'spec name 1',
      id: 'spec id 1',
      version: 'version 1',
      // eslint-disable-next-line @typescript-eslint/naming-convention
      model_count: 1,
    };
    component.specInfo = specInfo;

    // WHEN changes are detected
    fixture.detectChanges();

    // THEN no paragraph elements are shown
    const ps: NodeListOf<HTMLParagraphElement> = fixture.nativeElement.querySelectorAll(
      'p'
    );
    expect(ps.length).toEqual(2);
    expect(ps.item(0).innerText).toContain(specInfo.name);
    expect(ps.item(1).innerText).toContain(specInfo.id);
  });
});
