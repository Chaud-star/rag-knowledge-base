const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const uploadMessage = document.getElementById("uploadMessage");
const refreshBtn = document.getElementById("refreshBtn");
const documentList = document.getElementById("documentList");
const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");
const answerBox = document.getElementById("answerBox");
const wikiQuestionInput = document.getElementById("wikiQuestionInput");
const wikiAskBtn = document.getElementById("wikiAskBtn");
const wikiAnswerBox = document.getElementById("wikiAnswerBox");

async function loadDocuments() {
    const response = await fetch("/api/documents");
    const documents = await response.json();
    documentList.innerHTML = "";

    documents.forEach((doc) => {
        const li = document.createElement("li");
        li.textContent = doc.filename + " ";

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "删除";
        deleteBtn.onclick = () => deleteDocument(doc.document_id);
        li.appendChild(deleteBtn);
        documentList.appendChild(li);
    });

    if (documents.length === 0) {
        documentList.innerHTML = "<li>暂无文档</li>";
    }
}

async function uploadDocument() {
    if (!fileInput.files.length) {
        uploadMessage.textContent = "请先选择文件";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    uploadMessage.textContent = "上传中...";

    const response = await fetch("/api/documents/upload", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();
    uploadMessage.textContent = response.ok
        ? `上传成功：${result.filename}`
        : `上传失败：${result.detail}`;

    fileInput.value = "";
    loadDocuments();
}

async function deleteDocument(documentId) {
    await fetch(`/api/documents/${documentId}`, { method: "DELETE" });
    loadDocuments();
}

async function askQuestion() {
    const question = questionInput.value.trim();
    if (!question) {
        answerBox.textContent = "请输入问题";
        return;
    }

    answerBox.textContent = "正在生成答案...";

    const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });

    const result = await response.json();
    if (!response.ok) {
        answerBox.textContent = result.detail || "请求失败";
        return;
    }

    let text = `回答：\n${result.answer}\n\n引用来源：\n`;
    result.sources.forEach((source) => {
        text += `- ${source.document_id}\n  ${source.text}\n`;
    });

    answerBox.textContent = text;
}
async function askWikiQuestion() {
    const question = wikiQuestionInput.value.trim();
    if (!question) {
        wikiAnswerBox.textContent = "请输入问题";
        return;
    }

    wikiAnswerBox.textContent = "正在搜索维基百科并生成答案...";

    const response = await fetch("/api/chat_wiki", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });

    const result = await response.json();
    if (!response.ok) {
        wikiAnswerBox.textContent = result.detail || "请求失败";
        return;
    }

    let text = `回答：\n${result.answer}\n\n来源：\n`;
    result.sources.forEach((source) => {
        text += `- ${source.title}\n  ${source.url}\n  ${source.text.slice(0, 150)}\n`;
    });

    wikiAnswerBox.textContent = text;
}
uploadBtn.addEventListener("click", uploadDocument);
refreshBtn.addEventListener("click", loadDocuments);
askBtn.addEventListener("click", askQuestion);
wikiAskBtn.addEventListener("click", askWikiQuestion);

loadDocuments();