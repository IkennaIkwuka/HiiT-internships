import os
import zipfile

# Create folder structure
base_dir = "/mnt/data/paylink_demo"
os.makedirs(base_dir, exist_ok=True)

# Create a simple index.html that uses CDN React + Tailwind + Babel and inline JS
index_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PayLink — Offline Fintech Demo</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/qrcode/build/qrcode.min.js"></script>
    <script src="https://unpkg.com/react-qr-reader@3.0.0-beta.2/dist/index.umd.js"></script>
  </head>
  <body class="bg-teal-50">
    <div id="root"></div>
    <script type="text/babel" data-type="module">
      const { useState, useEffect } = React;
      const { QrReader } = window.ReactQrReader;
      const QRCode = window.QRCode;
      function PayLink() {
        const [route, setRoute] = useState('home');
        const [balance, setBalance] = useState(1250.35);
        const [pending, setPending] = useState([]);
        const [history, setHistory] = useState([]);
        const [sendAmount, setSendAmount] = useState('');
        const [qr, setQr] = useState('');
        const [payload, setPayload] = useState('');
        const [scanResult, setScanResult] = useState(null);
        const [scanning, setScanning] = useState(false);

        async function generateQR() {
          if (!sendAmount || Number(sendAmount) <= 0) return alert('Enter a valid amount');
          const data = { from: 'You', to: 'Receiver', amount: sendAmount, ts: new Date().toISOString() };
          const encoded = btoa(JSON.stringify(data));
          const url = await QRCode.toDataURL(encoded);
          setQr(url);
          setPayload(encoded);
          setPending([...pending, { ...data, status: 'Pending' }]);
        }

        function handleScan(result) {
          if (!result) return;
          try {
            const decoded = JSON.parse(atob(result));
            setHistory([{ ...decoded, status: 'Received' }, ...history]);
            alert(`₦${decoded.amount} received from ${decoded.from}`);
            setScanning(false);
          } catch (e) {
            alert('Invalid QR');
          }
        }

        function syncAll() {
          setHistory([...history, ...pending.map(p => ({ ...p, status: 'Completed' }))]);
          setPending([]);
          alert('All offline payments synced successfully!');
        }

        const colors = { primary: 'from-teal-600 to-emerald-500' };

        const Nav = () => (
          <nav className={`flex justify-between items-center p-4 bg-gradient-to-r ${colors.primary} text-white rounded-b-2xl`}>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-white text-teal-600 font-bold flex items-center justify-center rounded-full">P</div>
              <div className="font-semibold text-lg">PayLink</div>
            </div>
            <div className="flex gap-3">
              {['home', 'send', 'receive', 'history'].map(tab => (
                <button key={tab} onClick={() => setRoute(tab)} className={`capitalize ${route === tab ? 'underline font-semibold' : ''}`}>{tab}</button>
              ))}
            </div>
          </nav>
        );

        const Home = () => (
          <div className="p-6 space-y-6">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-teal-700">PayLink Wallet</h1>
              <p className="text-sm text-gray-500">No Network? No Problem.</p>
            </div>
            <div className="rounded-2xl bg-white p-6 shadow">
              <div className="text-gray-500 text-sm">Balance</div>
              <div className="text-4xl font-bold text-teal-700">₦{balance.toLocaleString()}</div>
            </div>
            {pending.length > 0 && (
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-center">
                {pending.length} offline transactions pending.
                <button onClick={syncAll} className="ml-2 text-amber-600 underline">Go Online & Sync</button>
              </div>
            )}
            <div className="grid grid-cols-2 gap-4">
              <button onClick={() => setRoute('send')} className={`py-3 rounded-xl bg-gradient-to-r ${colors.primary} text-white font-semibold shadow`}>Send</button>
              <button onClick={() => setRoute('receive')} className="py-3 rounded-xl bg-white shadow font-semibold text-teal-700 border border-teal-100">Receive</button>
            </div>
          </div>
        );

        const Send = () => (
          <div className="p-6 space-y-6">
            <h2 className="text-xl font-bold text-teal-700">Send Money</h2>
            <input type="number" placeholder="Amount (₦)" value={sendAmount} onChange={e => setSendAmount(e.target.value)} className="w-full p-3 border rounded" />
            <button onClick={generateQR} className={`w-full py-3 rounded-xl bg-gradient-to-r ${colors.primary} text-white font-semibold`}>Generate QR</button>
            {qr && (
              <div className="flex flex-col items-center">
                <img src={qr} alt="QR" className="w-48 h-48 bg-white p-2 rounded shadow" />
                <p className="text-xs text-gray-400 break-all mt-2">{payload}</p>
              </div>
            )}
          </div>
        );

        const Receive = () => (
          <div className="p-6 space-y-6">
            <h2 className="text-xl font-bold text-teal-700">Receive Money</h2>
            <div className="space-y-2">
              <button onClick={() => setScanning(!scanning)} className={`w-full py-3 rounded-xl ${scanning ? 'bg-red-100 text-red-700' : 'bg-gradient-to-r '+colors.primary+' text-white font-semibold'}`}>{scanning ? 'Stop Scanner' : 'Start Scanner'}</button>
            </div>
            {scanning && (
              <div className="mt-4 border rounded overflow-hidden">
                <QrReader constraints={{ facingMode: 'environment' }} onResult={(r) => { if (r?.text) handleScan(r.text); }} containerStyle={{ width: '100%' }} />
              </div>
            )}
          </div>
        );

        const History = () => (
          <div className="p-6 space-y-4">
            <h2 className="text-xl font-bold text-teal-700">Transaction History</h2>
            {[...history, ...pending].length === 0 && <p className="text-gray-400 text-sm">No transactions yet.</p>}
            {[...pending, ...history].map((t, i) => (
              <div key={i} className="flex justify-between bg-white p-3 rounded shadow">
                <div>
                  <div className="text-sm font-semibold">₦{t.amount}</div>
                  <div className="text-xs text-gray-500">{t.from} → {t.to}</div>\n                </div>
                <div className={`text-xs font-semibold ${t.status === 'Pending' ? 'text-yellow-600' : 'text-green-600'}`}>{t.status}</div>
              </div>
            ))}
          </div>
        );

        return (
          <div className="min-h-screen bg-gradient-to-b from-white to-teal-50 text-slate-800 max-w-sm mx-auto rounded-xl overflow-hidden shadow-xl border border-teal-100">
            <Nav />
            {route === 'home' && <Home />}
            {route === 'send' && <Send />}
            {route === 'receive' && <Receive />}
            {route === 'history' && <History />}
            <footer className="text-center text-xs text-gray-400 py-4">PayLink © 2025 — Offline Fintech Prototype</footer>
          </div>
        );
      }
      ReactDOM.createRoot(document.getElementById('root')).render(<PayLink/>);
    </script>
  </body>
</html>
"""

with open(os.path.join(base_dir, "index.html"), "w") as f:
    f.write(index_html)

# Create ZIP
zip_path = "/mnt/data/PayLink_Web_Demo.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    for foldername, _, filenames in os.walk(base_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            zipf.write(file_path, os.path.relpath(file_path, base_dir))

# zip_path
