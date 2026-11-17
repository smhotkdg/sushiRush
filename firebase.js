// Firebase 연결: 닉네임 등록과 무한 모드 전체 순위.
// 빌드 없이 쓰려고 gstatic CDN 의 모듈 SDK 를 불러온다. index.html 은 window.fbApi 로 접근한다.
// 아래 값은 공개용 웹 설정이다. 접근 제어는 firestore.rules 가 맡는다.
import { initializeApp } from "https://www.gstatic.com/firebasejs/13.2.0/firebase-app.js";
import { getAuth, signInAnonymously } from "https://www.gstatic.com/firebasejs/13.2.0/firebase-auth.js";
import {
  getFirestore, collection, doc, getDoc, getDocs, writeBatch, setDoc,
  query, where, orderBy, limit, getCountFromServer, serverTimestamp,
} from "https://www.gstatic.com/firebasejs/13.2.0/firebase-firestore.js";

const firebaseConfig = {
  "apiKey": "AIzaSyCaEcO5pccRdd-ml5j4UTc_l47_ixoQqcI",
  "authDomain": "sushirush-3cf7f.firebaseapp.com",
  "projectId": "sushirush-3cf7f",
  "storageBucket": "sushirush-3cf7f.firebasestorage.app",
  "messagingSenderId": "826542911309",
  "appId": "1:826542911309:web:df2200b76af321ca6cd104",
  "measurementId": "G-8QCWCJ3VTC"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Firestore 규칙은 로그인된 요청만 받는다. 게임 계정(카카오·네이버·구글)과 별개로 익명 로그인을 유지한다.
let signingIn = null;
async function ready() {
  await auth.authStateReady();
  if (auth.currentUser) return auth.currentUser;
  signingIn ||= signInAnonymously(auth).finally(() => { signingIn = null; });
  return (await signingIn).user;
}
const nickKey = (n) => n.toLowerCase();

// 플레이어(게임 계정) 정보. 없으면 null.
async function getPlayer(pid) {
  await ready();
  const s = await getDoc(doc(db, "players", pid));
  return s.exists() ? s.data() : null;
}

// 닉네임 등록. 닉네임은 전체에서 하나뿐이고, 한 번 정하면 바뀌지 않는다.
async function createPlayer(pid, provider, nickname) {
  await ready();
  const taken = await getDoc(doc(db, "nicknames", nickKey(nickname)));
  if (taken.exists()) return { ok: false, reason: taken.data().pid === pid ? "mine" : "taken" };
  const b = writeBatch(db);
  b.set(doc(db, "players", pid), { pid, provider, nickname, createdAt: serverTimestamp() });
  b.set(doc(db, "nicknames", nickKey(nickname)), { pid, createdAt: serverTimestamp() });
  try { await b.commit(); return { ok: true }; }
  catch (e) {                                     // 동시에 같은 닉네임을 잡은 경우 등
    const again = await getDoc(doc(db, "nicknames", nickKey(nickname)));
    if (again.exists() && again.data().pid !== pid) return { ok: false, reason: "taken" };
    throw e;
  }
}

// 상위 n개 (점수 내림차순)
async function top(n = 10) {
  await ready();
  const snap = await getDocs(query(collection(db, "leaderboard"), orderBy("score", "desc"), limit(n)));
  return snap.docs.map((d) => d.data());
}

// 내 최고 기록과 순위
async function mine(pid) {
  await ready();
  const s = await getDoc(doc(db, "leaderboard", pid));
  if (!s.exists()) return null;
  const e = s.data();
  const higher = await getCountFromServer(query(collection(db, "leaderboard"), where("score", ">", e.score)));
  return { ...e, rank: higher.data().count + 1 };
}

// 기록 제출. 내 최고 기록보다 높을 때만 저장한다(규칙도 같은 조건을 강제한다).
async function submit(pid, name, { score, time, served }) {
  await ready();
  const ref = doc(db, "leaderboard", pid);
  const prev = await getDoc(ref);
  const best = prev.exists() ? prev.data().score : -1;
  if (score <= best) return { improved: false, best };
  await setDoc(ref, {
    pid, name,
    score: Math.max(0, Math.floor(score)),
    time: Math.max(0, Math.min(86400, Math.floor(time))),
    served: Math.max(0, Math.floor(served)),
    updatedAt: serverTimestamp(),
  });
  return { improved: true, best: score };
}

window.fbApi = { ready, getPlayer, createPlayer, top, mine, submit, uid: () => auth.currentUser?.uid || null };
window.dispatchEvent(new Event("fb-ready"));
