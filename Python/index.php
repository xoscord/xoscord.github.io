<?php
// ====== CONFIG ======
$owner = "xoscord";
$repo  = "xoscord.github.io";
$path  = "Python";
$branch = "main";

// ====== GET FILE LIST FROM GITHUB ======
$apiUrl = "https://api.github.com/repos/$owner/$repo/contents/$path?ref=$branch";

$context = stream_context_create([
    "http" => [
        "method" => "GET",
        "header" => "User-Agent: PHP"
    ]
]);

$response = @file_get_contents($apiUrl, false, $context);
$files = [];

if ($response) {
    $data = json_decode($response, true);
    foreach ($data as $item) {
        if ($item["type"] === "file" && pathinfo($item["name"], PATHINFO_EXTENSION) === "py") {
            $files[] = $item["name"];
        }
    }
}

$currentFile = isset($_GET['file']) ? basename($_GET['file']) : null;
$content = "";

if ($currentFile && in_array($currentFile, $files)) {
    $rawUrl = "https://raw.githubusercontent.com/$owner/$repo/$branch/$path/$currentFile";
    $code = @file_get_contents($rawUrl, false, $context);
    $content = $code ? htmlspecialchars($code) : "❌ Failed to load file.";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="icon" type="image/svg+xml"
  href='data:image/svg+xml,
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="32" fill="none"
            stroke="%233776AB" stroke-width="20"/>
  </svg>'>

<title>Python Code Viewer</title>

<style>
@font-face {
  font-family: 'font5';
  src: url('/share/font5.ttf') format('truetype');
}
@font-face {
  font-family: 'font';
  src: url('/share/font.ttf') format('truetype');
}
body {
  margin: 0;
  padding: 1rem;
  background: #0d1117;
  color: #e6edf3;
  font-family: system-ui, sans-serif;
}
h1 {
  font-size: 1.4rem;
  margin-bottom: 1rem;
  font-family: font5;
}
#fileList button {
  width: 100%;
  padding: 0.9rem 1rem;
  margin-bottom: 0.6rem;
  border-radius: 12px;
  background: #161b22;
  border: 1px solid #30363d;
  color: #e6edf3;
  font-size: 1rem;
  cursor: pointer;
  font-family: font;
}
#fileList button:hover {
  background: #1f2937;
}
#viewerPanel {
  <?php if ($currentFile) echo "display:block; position:fixed; inset:0;"; else echo "display:none;"; ?>
  background: #0d1117;
  padding: 1rem;
  animation: slideUp 0.25s ease;
}
@keyframes slideUp {
  from { transform: translateY(100%); }
  to   { transform: translateY(0); }
}
.viewer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.6rem;
  margin-bottom: 0.6rem;
}
.filename {
  font-size: 0.85rem;
  color: #9da7b3;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.icon-btn {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 10px;
  padding: 0.45rem 0.6rem;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.icon-btn svg {
  width: 18px;
  height: 18px;
  fill: #e6edf3;
  transition: transform 0.2s ease, fill 0.2s ease;
}
.icon-btn.copied svg {
  fill: #3fb950;
  transform: scale(1.15);
}
pre {
  height: calc(100vh - 120px);
  margin: 0;
  padding: 1rem;
  background: #010409;
  border: 1px solid #30363d;
  border-radius: 12px;
  overflow: auto;
  font-size: 0.85rem;
  line-height: 1.5;
  white-space: pre;
}
</style>
</head>

<body>

<h1>☯ Python Programs</h1>

<?php if (!$currentFile): ?>
<div id="fileList">
  <?php if ($files): ?>
    <?php foreach ($files as $file): ?>
      <button onclick="location.href='?file=<?php echo urlencode($file); ?>'">
        <?php echo htmlspecialchars($file); ?>
      </button>
    <?php endforeach; ?>
  <?php else: ?>
    <p>❌ No Python files found.</p>
  <?php endif; ?>
</div>
<?php endif; ?>

<?php if ($currentFile): ?>
<div id="viewerPanel">
  <div class="viewer-header">
    <button class="icon-btn" onclick="location.href='index.php'" title="Back">
      <svg viewBox="0 0 24 24">
        <path d="M15 18l-6-6 6-6"/>
      </svg>
    </button>

    <div class="filename"><?php echo htmlspecialchars($currentFile); ?></div>

    <button class="icon-btn" id="copyBtn" onclick="copyCode()" title="Copy">
      <svg viewBox="0 0 24 24">
        <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8
        c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11
        c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2z"/>
      </svg>
    </button>
  </div>

  <pre id="viewer"><?php echo $content; ?></pre>
</div>
<?php endif; ?>

<script>
function copyCode() {
  const text = document.getElementById("viewer").innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById("copyBtn");
    btn.classList.add("copied");
    setTimeout(() => btn.classList.remove("copied"), 800);
  });
}
</script>

</body>
</html>
