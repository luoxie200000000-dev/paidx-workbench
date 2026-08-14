// ============================================================
//  Web 预览数据引导（仅非 Tauri 环境执行）
//  将 mock-data.json 预载入 localStorage(pdx_workbench_v6)，
//  供 app.js 读取。Tauri 桌面环境自动跳过（使用真实 SQLite）。
//  使用同步 flag + async IIFE，app.js 通过轮询 flag 确保数据就绪。
// ============================================================
if (!(window.__IS_TAURI_APP__ || window.__TAURI_INTERNALS__)) {
  window.__WEB_PREVIEW__ = true;
  window.__WEB_PREVIEW_READY__ = false;
  (async () => {
    try {
      const resp = await fetch('./mock-data.json');
      const mockData = await resp.json();
      localStorage.setItem('pdx_workbench_v6', JSON.stringify(mockData));
      window.__WEB_PREVIEW_READY__ = true;
      console.log('[Web Preview] mock data loaded into localStorage (' + JSON.stringify(mockData).length + ' bytes)');
    } catch (e) {
      window.__WEB_PREVIEW_READY__ = true;
      console.error('[Web Preview] mock data load failed:', e);
    }
  })();
}
