function prefersReducedMotion(): boolean {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function focusActivatedStage(root: ParentNode = document): void {
  const stage = root.querySelector<HTMLElement>(
    '[data-lx-focus-stage][data-focus-on-activation="true"]',
  );

  if (!stage) {
    return;
  }

  stage.focus({ preventScroll: true });
  stage.scrollIntoView({
    behavior: prefersReducedMotion() ? 'auto' : 'smooth',
    block: 'start',
  });
}
