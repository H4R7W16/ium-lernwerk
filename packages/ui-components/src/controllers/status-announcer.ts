export type StateStatusDetail = Readonly<{
  state: 'saving' | 'saved' | 'volatile' | 'deleted' | 'imported';
  mode: 'persistent' | 'volatile-selected' | 'volatile-fallback';
  message: string;
}>;

export type ErrorDetail = Readonly<{
  code: string;
  message: string;
  action: string;
  technicalDetails?: string;
}>;

export type DataChangedDetail = Readonly<{
  scope: 'module' | 'all';
  operation: 'save' | 'import' | 'delete';
}>;

export function announceState(
  target: EventTarget,
  detail: StateStatusDetail,
): void {
  target.dispatchEvent(new CustomEvent<StateStatusDetail>('ium:state-status', { detail }));
}

export function announceError(target: EventTarget, detail: ErrorDetail): void {
  target.dispatchEvent(new CustomEvent<ErrorDetail>('ium:error', { detail }));
}

export function announceDataChanged(
  target: EventTarget,
  detail: DataChangedDetail,
): void {
  target.dispatchEvent(new CustomEvent<DataChangedDetail>('ium:data-changed', { detail }));
}

export function connectStatusAnnouncers(root: ParentNode = document): void {
  document.addEventListener('ium:state-status', ((event: CustomEvent<StateStatusDetail>) => {
    for (const target of root.querySelectorAll<HTMLElement>('[data-storage-status]')) {
      target.textContent = event.detail.message;
    }
  }) as EventListener);
  document.addEventListener('ium:error', ((event: CustomEvent<ErrorDetail>) => {
    const summary = root.querySelector<HTMLElement>('[data-error-summary]');
    if (!summary) {
      return;
    }
    summary.hidden = false;
    const message = summary.querySelector<HTMLElement>('[data-error-message]');
    const action = summary.querySelector<HTMLElement>('[data-error-action]');
    const details = summary.querySelector<HTMLElement>('[data-error-details]');
    if (message) message.textContent = event.detail.message;
    if (action) action.textContent = event.detail.action;
    if (details) {
      details.textContent = [event.detail.code, event.detail.technicalDetails]
        .filter(Boolean)
        .join('\n');
    }
    summary.focus();
  }) as EventListener);
}
