import sys
import re

def main():
    file_path = r'c:\Users\ACER\Downloads\Promodo-web-main\Promodo-web-main\index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We will replace AudioEngine block
    audio_engine_replacement = """        // ===== Web Audio API Ambient Sound Generator =====
        const AudioEngine = (() => {
            let ctx = null;
            let masterGain = null;
            let activeNodes = {};

            function getCtx() {
                if (!ctx) {
                    ctx = new (window.AudioContext || window.webkitAudioContext)();
                    masterGain = ctx.createGain();
                    masterGain.connect(ctx.destination);
                    masterGain.gain.value = 0.65;
                }
                if (ctx.state === 'suspended') ctx.resume();
                return { ac: ctx, out: masterGain };
            }

            function createNoiseBuffer(ac, duration = 2) {
                const sampleRate = ac.sampleRate;
                const length = sampleRate * duration;
                const buffer = ac.createBuffer(2, length, sampleRate);
                for (let ch = 0; ch < 2; ch++) {
                    const data = buffer.getChannelData(ch);
                    for (let i = 0; i < length; i++) {
                        data[i] = Math.random() * 2 - 1;
                    }
                }
                return buffer;
            }

            function startRain(ac, out) {
                const gain = ac.createGain();
                gain.gain.value = 0.35;
                gain.connect(out);

                const noiseSource = ac.createBufferSource();
                noiseSource.buffer = createNoiseBuffer(ac, 2);
                noiseSource.loop = true;
                const bp = ac.createBiquadFilter();
                bp.type = 'bandpass';
                bp.frequency.value = 800;
                bp.Q.value = 0.5;
                noiseSource.connect(bp);
                bp.connect(gain);
                noiseSource.start();

                const rumble = ac.createBufferSource();
                rumble.buffer = createNoiseBuffer(ac, 2);
                rumble.loop = true;
                const lp = ac.createBiquadFilter();
                lp.type = 'lowpass';
                lp.frequency.value = 150;
                const rumbleGain = ac.createGain();
                rumbleGain.gain.value = 0.15;
                rumble.connect(lp);
                lp.connect(rumbleGain);
                rumbleGain.connect(out);
                rumble.start();

                return { nodes: [noiseSource, rumble, bp, lp, gain, rumbleGain], stop() { noiseSource.stop(); rumble.stop(); gain.disconnect(); rumbleGain.disconnect(); } };
            }

            function startCoffee(ac, out) {
                const gain = ac.createGain();
                gain.gain.value = 0.25;
                gain.connect(out);

                const bufLen = ac.sampleRate * 2;
                const buffer = ac.createBuffer(2, bufLen, ac.sampleRate);
                for (let ch = 0; ch < 2; ch++) {
                    const data = buffer.getChannelData(ch);
                    let last = 0;
                    for (let i = 0; i < bufLen; i++) {
                        const white = Math.random() * 2 - 1;
                        data[i] = (last + 0.02 * white) / 1.02;
                        last = data[i];
                        data[i] *= 3.5;
                    }
                }
                const brown = ac.createBufferSource();
                brown.buffer = buffer;
                brown.loop = true;
                const bp = ac.createBiquadFilter();
                bp.type = 'bandpass';
                bp.frequency.value = 500;
                bp.Q.value = 0.3;
                brown.connect(bp);
                bp.connect(gain);
                brown.start();

                const chatter = ac.createBufferSource();
                chatter.buffer = createNoiseBuffer(ac, 2);
                chatter.loop = true;
                const chatterBP = ac.createBiquadFilter();
                chatterBP.type = 'bandpass';
                chatterBP.frequency.value = 2000;
                chatterBP.Q.value = 1.5;
                const chatterGain = ac.createGain();
                chatterGain.gain.value = 0.06;
                chatter.connect(chatterBP);
                chatterBP.connect(chatterGain);
                chatterGain.connect(out);
                chatter.start();

                const clinkGain = ac.createGain();
                clinkGain.gain.value = 0.0;
                clinkGain.connect(out);
                const clinkInterval = setInterval(() => {
                    if (Math.random() > 0.6) {
                        const osc = ac.createOscillator();
                        osc.frequency.value = 2000 + Math.random() * 3000;
                        osc.type = 'sine';
                        const envGain = ac.createGain();
                        envGain.gain.setValueAtTime(0.03, ac.currentTime);
                        envGain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.15);
                        osc.connect(envGain);
                        envGain.connect(out);
                        osc.start();
                        osc.stop(ac.currentTime + 0.15);
                    }
                }, 800);

                return { nodes: [brown, chatter, bp, chatterBP, gain, chatterGain, clinkGain], stop() { brown.stop(); chatter.stop(); clearInterval(clinkInterval); gain.disconnect(); chatterGain.disconnect(); clinkGain.disconnect(); } };
            }

            function startWaves(ac, out) {
                const gain = ac.createGain();
                gain.gain.value = 0.3;
                gain.connect(out);

                const noise = ac.createBufferSource();
                noise.buffer = createNoiseBuffer(ac, 4);
                noise.loop = true;

                const lfo = ac.createOscillator();
                lfo.type = 'sine';
                lfo.frequency.value = 0.12; 
                const lfoGain = ac.createGain();
                lfoGain.gain.value = 0.4;
                lfo.connect(lfoGain);

                const lp = ac.createBiquadFilter();
                lp.type = 'lowpass';
                lp.frequency.value = 600;

                const modGain = ac.createGain();
                modGain.gain.value = 0.6;
                lfoGain.connect(modGain.gain);

                noise.connect(lp);
                lp.connect(modGain);
                modGain.connect(gain);
                lfo.start();
                noise.start();

                const hiss = ac.createBufferSource();
                hiss.buffer = createNoiseBuffer(ac, 2);
                hiss.loop = true;
                const hp = ac.createBiquadFilter();
                hp.type = 'highpass';
                hp.frequency.value = 3000;
                const hissGain = ac.createGain();
                hissGain.gain.value = 0.05;
                hiss.connect(hp);
                hp.connect(hissGain);
                hissGain.connect(out);
                hiss.start();

                return { nodes: [noise, lfo, lp, gain, lfoGain, modGain, hiss, hp, hissGain], stop() { noise.stop(); lfo.stop(); hiss.stop(); gain.disconnect(); hissGain.disconnect(); } };
            }

            function startForest(ac, out) {
                const gain = ac.createGain();
                gain.gain.value = 0.15;
                gain.connect(out);

                const wind = ac.createBufferSource();
                wind.buffer = createNoiseBuffer(ac, 3);
                wind.loop = true;
                const bp = ac.createBiquadFilter();
                bp.type = 'bandpass';
                bp.frequency.value = 300;
                bp.Q.value = 0.8;
                wind.connect(bp);
                bp.connect(gain);
                wind.start();

                const cricketIntervals = [];
                function chirp() {
                    const osc = ac.createOscillator();
                    osc.type = 'sine';
                    osc.frequency.value = 4000 + Math.random() * 2000;
                    const envGain = ac.createGain();
                    const now = ac.currentTime;
                    envGain.gain.setValueAtTime(0, now);

                    const chirpCount = 2 + Math.floor(Math.random() * 4);
                    for (let i = 0; i < chirpCount; i++) {
                        envGain.gain.setValueAtTime(0.04, now + i * 0.07);
                        envGain.gain.setValueAtTime(0, now + i * 0.07 + 0.03);
                    }
                    osc.connect(envGain);
                    envGain.connect(out);
                    osc.start();
                    osc.stop(now + chirpCount * 0.07 + 0.1);
                }

                cricketIntervals.push(setInterval(() => { if (Math.random() > 0.4) chirp(); }, 600));
                cricketIntervals.push(setInterval(() => { if (Math.random() > 0.5) chirp(); }, 1100));

                return { nodes: [wind, bp, gain], stop() { wind.stop(); cricketIntervals.forEach(clearInterval); gain.disconnect(); } };
            }

            function startWhiteNoise(ac, out) {
                const gain = ac.createGain();
                gain.gain.value = 0.2;
                gain.connect(out);

                const noise = ac.createBufferSource();
                noise.buffer = createNoiseBuffer(ac, 2);
                noise.loop = true;
                noise.connect(gain);
                noise.start();

                return { nodes: [noise, gain], stop() { noise.stop(); gain.disconnect(); } };
            }

            return {
                start(soundId) {
                    const { ac, out } = getCtx();
                    const starters = { rain: startRain, coffee: startCoffee, waves: startWaves, forest: startForest, noise: startWhiteNoise };
                    if (starters[soundId]) {
                        activeNodes[soundId] = starters[soundId](ac, out);
                    }
                },
                stop(soundId) {
                    if (activeNodes[soundId]) {
                        try { activeNodes[soundId].stop(); } catch (e) { }
                        delete activeNodes[soundId];
                    }
                },
                stopAll() {
                    Object.keys(activeNodes).forEach(id => this.stop(id));
                },
                setVolume(vol) {
                    if (masterGain) {
                        masterGain.gain.value = Math.max(0, Math.min(1, vol));
                    }
                }
            };
        })();"""

    app_replacement = """        function App() {
            const [activeTab, setActiveTab] = useState('dashboard');

            const [durations, setDurations] = useState({ focus: 25, shortBreak: 5, longBreak: 15 });
            const [showTimeEditor, setShowTimeEditor] = useState(false);

            const [mode, setMode] = useState('focus');
            const [timeLeft, setTimeLeft] = useState(durations.focus * 60);
            const [isActive, setIsActive] = useState(false);

            const [stats, setStats] = useState({ focusMinutesToday: 0, streak: 0, distractions: 0 });

            const [quote, setQuote] = useState(QUOTE_LIBRARY[0]);
            const [ytLinkInput, setYtLinkInput] = useState('');
            const [ytEmbedUrl, setYtEmbedUrl] = useState('');
            const [activeSound, setActiveSound] = useState(null);
            const [volume, setVolume] = useState(65);

            useEffect(() => {
                AudioEngine.setVolume(volume / 100);
            }, [volume]);

            const adjustDuration = (key, delta) => {
                const limits = { focus: [1, 120], shortBreak: [1, 30], longBreak: [1, 60] };
                setDurations(prev => {
                    const newVal = Math.max(limits[key][0], Math.min(limits[key][1], prev[key] + delta));
                    return { ...prev, [key]: newVal };
                });
            };

            const tickRef = useRef(null);

            const toggleSound = (soundId) => {
                AudioEngine.stopAll();
                if (activeSound === soundId) {
                    setActiveSound(null);
                } else {
                    AudioEngine.start(soundId);
                    AudioEngine.setVolume(volume / 100);
                    setActiveSound(soundId);
                }
            };

            const applyYoutube = () => {
                try {
                    let videoId = '';
                    if (ytLinkInput.includes('youtu.be/')) {
                        videoId = ytLinkInput.split('youtu.be/')[1].split('?')[0];
                    } else if (ytLinkInput.includes('youtube.com/watch')) {
                        videoId = new URLSearchParams(ytLinkInput.split('?')[1]).get('v');
                    }
                    if (videoId) {
                        setYtEmbedUrl(`https://www.youtube.com/embed/${videoId}?autoplay=1`);
                    } else {
                        alert('Vui lòng nhập link YouTube hợp lệ!');
                    }
                } catch (e) {
                    alert('Lỗi khi xử lý link!');
                }
            };

            useEffect(() => {
                if (!isActive) {
                    setTimeLeft(durations[mode] * 60);
                }
            }, [durations, mode, isActive]);

            useEffect(() => {
                if (isActive && timeLeft > 0) {
                    tickRef.current = setInterval(() => setTimeLeft(t => t - 1), 1000);
                } else if (timeLeft === 0 && isActive) {
                    clearInterval(tickRef.current);
                    setIsActive(false);
                    if (mode === 'focus') {
                        setStats(s => ({ ...s, focusMinutesToday: s.focusMinutesToday + durations.focus, streak: s.streak === 0 ? 1 : s.streak }));
                        setQuote(QUOTE_LIBRARY[Math.floor(Math.random() * QUOTE_LIBRARY.length)]);
                    }
                }
                return () => clearInterval(tickRef.current);
            }, [isActive, timeLeft, mode, durations]);

            const handleSwitchMode = (newMode) => {
                setIsActive(false);
                setMode(newMode);
                setTimeLeft(durations[newMode] * 60);
            };

            const toggleTimer = () => setIsActive(!isActive);
            const resetTimer = () => {
                setIsActive(false);
                setTimeLeft(durations[mode] * 60);
            };

            const formatTime = (seconds) => {
                const m = Math.floor(seconds / 60);
                const s = seconds % 60;
                return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
            };

            const totalSecs = durations[mode] * 60;
            const progressOffset = ((totalSecs - timeLeft) / totalSecs) * 100;
            const circleRadius = 48;
            const circumference = 2 * Math.PI * circleRadius;
            const strokeDashoffset = (progressOffset / 100) * circumference;

            return (
                <div className="flex h-screen bg-[#F8F9FB] font-sans overflow-hidden text-slate-800">
                    {/* Left Sidebar */}
                    <div className="w-[300px] flex flex-col flex-shrink-0 h-full py-10 border-r border-slate-200/50 bg-[#F4F6F9]">
                        <div className="px-10 mb-8">
                            <h1 className="font-extrabold text-[22px] text-[#2D3748] tracking-tight leading-tight">Smart Focus</h1>
                            <p className="text-[10px] font-bold text-slate-400 tracking-[0.15em] mt-1">DIGITAL SANCTUARY</p>
                        </div>

                        <nav className="flex flex-col gap-2 flex-1 px-4 mt-6">
                            {[
                                { id: 'dashboard', icon: 'LayoutGrid', label: 'Dashboard' },
                                { id: 'timer', icon: 'Clock', label: 'Focus Timer' },
                                { id: 'stats', icon: 'BarChart2', label: 'Analytics' },
                                { id: 'sounds', icon: 'AudioLines', label: 'Soundscapes' },
                                { id: 'library', icon: 'BookOpen', label: 'Library' }
                            ].map(item => (
                                <button key={item.id} onClick={() => setActiveTab(item.id)}
                                    className={`relative flex items-center gap-4 px-6 py-4 rounded-full font-bold text-[15px] transition-all
                                    ${activeTab === item.id
                                            ? 'text-brand-600 bg-white shadow-soft'
                                            : 'text-slate-500 hover:bg-white/50 hover:text-slate-700'}`}>
                                    <Icon name={item.icon} size={20} className={activeTab === item.id ? 'text-brand-600' : 'text-slate-500'} />
                                    {item.label}
                                    {activeTab === item.id && (
                                        <div className="absolute right-0 top-1/2 -translate-y-1/2 w-1.5 h-6 bg-brand-600 rounded-l-full shadow-[0_0_8px_rgba(79,70,229,0.6)]"></div>
                                    )}
                                </button>
                            ))}
                        </nav>
                        <div className="flex flex-col gap-2 mt-auto px-6">
                            <button className="bg-[#6B63ED] text-white rounded-full py-4 font-bold text-[15px] w-full hover:bg-brand-600 transition-colors shadow-[0_8px_20px_-4px_rgba(107,99,237,0.4)] mb-6">
                                Start Session
                            </button>
                            <button className="flex items-center gap-4 px-6 py-3 font-semibold text-[15px] text-slate-500 hover:text-slate-800 transition-all">
                                <Icon name="HelpCircle" size={20} className="text-slate-600" /> Support
                            </button>
                            <button className="flex items-center gap-4 px-6 py-3 font-semibold text-[15px] text-slate-500 hover:text-slate-800 transition-all">
                                <Icon name="Settings" size={20} className="text-slate-600" /> Settings
                            </button>
                        </div>
                    </div>

                    {/* Main Content */}
                    <div className="flex-1 flex overflow-hidden">
                        
                        {/* Center Column - Timer View */}
                        <div className="flex-1 flex flex-col min-w-0 px-16 py-10 overflow-y-auto scrollbar-hide relative bg-[#F8F9FB]">
                            {/* Breadcrumb section */}
                            <div className="flex items-center gap-2 text-[14px] text-slate-500 mb-3 font-medium">
                                <span>Dashboard</span>
                                <Icon name="ChevronRight" size={14} className="text-slate-400" />
                                <span className="font-bold text-brand-600">Focus Timer</span>
                            </div>
                            <h2 className="text-[36px] font-black text-[#1E293B] tracking-tight mb-10">Deep Work Protocol</h2>

                            {/* Timer area */}
                            <div className="flex-1 flex flex-col items-center justify-center min-h-[420px] -mt-6">
                                <div className="relative w-[400px] h-[400px] flex flex-col items-center justify-center">
                                    <svg className="absolute w-full h-full transform -rotate-90">
                                        <circle cx="50%" cy="50%" r="48%" stroke="#E2E8F0" strokeWidth="12" fill="transparent" />
                                        <circle cx="50%" cy="50%" r="48%" stroke="#6B63ED" strokeWidth="12" fill="transparent"
                                            className="transition-all duration-1000 ease-linear"
                                            strokeDasharray={`${circumference}%`}
                                            strokeDashoffset={`${strokeDashoffset}%`}
                                            strokeLinecap="round" />
                                    </svg>
                                    <div className="flex flex-col items-center justify-center z-10 pt-4">
                                        <span className="font-black text-[84px] tracking-tighter text-[#1A202C] leading-none mb-3">{formatTime(timeLeft)}</span>
                                        <span className="text-[14px] font-bold text-[#6B63ED] tracking-[0.15em] uppercase">{mode === 'focus' ? 'FOCUS PHASE' : mode === 'shortBreak' ? 'SHORT BREAK' : 'LONG BREAK'}</span>
                                    </div>
                                </div>

                                <p className="mt-12 text-[15px] text-slate-400 font-medium italic text-center max-w-[360px]">"{quote}"</p>

                                <div className="flex items-center gap-6 mt-12">
                                    <button onClick={resetTimer} className="w-16 h-16 rounded-full bg-[#E2E8F0] flex items-center justify-center text-slate-600 hover:bg-slate-300 transition-colors group">
                                        <Icon name="RotateCcw" size={24} className="group-hover:-rotate-90 transition-transform duration-300" />
                                    </button>
                                    <button onClick={toggleTimer} className="w-[180px] h-16 bg-[#6B63ED] rounded-full flex items-center justify-center gap-3 text-white font-bold text-[16px] shadow-[0_10px_25px_-5px_rgba(107,99,237,0.5)] hover:bg-[#5a52da] hover:-translate-y-0.5 transition-all">
                                        <Icon name={isActive ? 'Pause' : 'Play'} size={22} className="fill-current" /> {isActive ? 'Tạm dừng' : 'Bắt đầu'}
                                    </button>
                                    <button onClick={() => setShowTimeEditor(!showTimeEditor)} className="w-16 h-16 rounded-full bg-[#E2E8F0] flex items-center justify-center text-slate-600 hover:bg-slate-300 transition-colors hover:rotate-90 duration-300">
                                        <Icon name="Settings" size={24} />
                                    </button>
                                </div>
                                {showTimeEditor && (
                                   <div className="absolute top-[45%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white/90 backdrop-blur p-6 rounded-3xl shadow-[0_20px_40px_-10px_rgba(0,0,0,0.1)] z-50 border border-slate-100 flex gap-6 animate-in fade-in zoom-in duration-200">
                                        {[
                                            { key: 'focus', label: 'Tập trung' },
                                            { key: 'shortBreak', label: 'Nghỉ ngắn' },
                                            { key: 'longBreak', label: 'Nghỉ dài' }
                                        ].map(item => (
                                            <div key={item.key} className="flex flex-col items-center gap-2">
                                                <span className="text-[11px] font-bold text-slate-400 tracking-widest uppercase">{item.label}</span>
                                                <div className="flex items-center gap-1 bg-[#F4F6F9] rounded-xl p-1 border border-slate-100">
                                                    <button onClick={() => adjustDuration(item.key, -1)} disabled={isActive}
                                                        className="w-8 h-8 rounded-lg bg-white shadow-sm flex items-center justify-center text-slate-600 text-lg font-bold hover:text-brand-600 transition-colors">−</button>
                                                    <span className="w-12 text-center font-mono font-bold text-lg text-slate-700">{durations[item.key]}</span>
                                                    <button onClick={() => adjustDuration(item.key, 1)} disabled={isActive}
                                                        className="w-8 h-8 rounded-lg bg-white shadow-sm flex items-center justify-center text-slate-600 text-lg font-bold hover:text-brand-600 transition-colors">+</button>
                                                </div>
                                            </div>
                                        ))}
                                   </div>
                                )}
                            </div>

                            {/* Distractions */}
                            <div className="mt-8 mb-4">
                                <h3 className="text-[24px] font-extrabold text-[#1E293B] mb-2">Bị xao nhãng?</h3>
                                <div className="flex items-center gap-4 mb-8">
                                    <p className="text-[15px] text-slate-500 font-medium">Ghi lại trạng thái tinh thần của bạn</p>
                                    <div className="flex-1 h-px bg-slate-200"></div>
                                </div>
                                <div className="flex gap-5">
                                    {[
                                        { id: 'social', icon: 'Network', label: 'Mạng\\nxã hội', badgeColor: 'text-[#6B63ED]', iconBg: 'bg-[#EEEDFC]' },
                                        { id: 'msg', icon: 'MessageSquare', label: 'Tin\\nnhắn', badgeColor: 'text-[#4299E1]', iconBg: 'bg-[#EBF8FF]' },
                                        { id: 'eat', icon: 'Utensils', label: 'Ăn\\nuống', badgeColor: 'text-[#ED64A6]', iconBg: 'bg-[#FFF5F7]' },
                                        { id: 'other', icon: 'MoreHorizontal', label: 'Khác', badgeColor: 'text-slate-500', iconBg: 'bg-slate-200' }
                                    ].map(d => (
                                        <button key={d.id} onClick={() => setStats(s => ({ ...s, distractions: s.distractions + 1 }))} 
                                            className="flex-1 bg-white rounded-[28px] p-6 flex flex-col items-center justify-center gap-4 shadow-soft hover:shadow-md hover:-translate-y-1 transition-all group">
                                            <div className={`w-16 h-16 rounded-2xl flex items-center justify-center ${d.badgeColor} ${d.iconBg} transform group-hover:scale-105 transition-transform`}>
                                                <Icon name={d.icon} size={28} strokeWidth={2.5} />
                                            </div>
                                            <span className="text-[15px] font-bold text-[#2D3748] text-center leading-tight whitespace-pre-line">{d.label.replace('\\\\n', '\\n')}</span>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Right Column - Tools */}
                        <div className="w-[380px] bg-white flex flex-col flex-shrink-0 border-l border-slate-200/50 p-8 shadow-[-10px_0_30px_rgba(0,0,0,0.02)] h-full overflow-y-auto scrollbar-hide z-10">
                            <div className="flex items-center gap-3 mb-5">
                                <Icon name="Youtube" size={24} className="text-[#FF0000] fill-current" />
                                <span className="font-extrabold text-[#1E293B] text-[18px]">YouTube Focus</span>
                            </div>
                            
                            <div className="mb-10 w-full">
                                {ytEmbedUrl ? (
                                    <div className="flex flex-col gap-3">
                                        <div className="relative w-full overflow-hidden rounded-[20px] bg-slate-100 border border-slate-200 aspect-video shadow-sm">
                                            <iframe src={ytEmbedUrl} className="absolute top-0 left-0 w-full h-full border-0" allow="autoplay; encrypted-media" allowFullScreen></iframe>
                                        </div>
                                        <button onClick={() => { setYtEmbedUrl(''); setYtLinkInput(''); }} className="text-[13px] text-red-500 font-bold hover:bg-red-50 py-2 rounded-xl text-center uppercase tracking-widest transition-colors w-full">Gỡ video</button>
                                    </div>
                                ) : (
                                    <div className="flex flex-col gap-4">
                                        <div className="relative w-full rounded-[20px] overflow-hidden bg-slate-100 aspect-video shadow-sm">
                                            <img src="https://images.unsplash.com/photo-1620025701838-8fa1b49f3e46?q=80&w=2564&auto=format&fit=crop" className="w-full h-full object-cover opacity-80 mix-blend-multiply" />
                                            <div className="absolute inset-0 flex items-center justify-center bg-[#8cb6cc]/10 backdrop-blur-[1px]">
                                                 <div className="w-14 h-14 bg-white/90 backdrop-blur rounded-full flex items-center justify-center shadow-lg text-slate-500">
                                                     <Icon name="Play" size={24} className="fill-current ml-1" />
                                                 </div>
                                            </div>
                                        </div>
                                        <input type="text" value={ytLinkInput} onChange={e => setYtLinkInput(e.target.value)} placeholder="Dán link YouTube tại đây..." className="w-full border border-slate-200 rounded-[14px] px-5 py-3.5 text-[14px] text-slate-600 outline-none focus:border-[#6B63ED] shadow-sm font-medium bg-white" />
                                        <button onClick={applyYoutube} className="w-full bg-[#F3F4FE] text-[#6B63ED] rounded-[14px] py-3.5 font-bold text-[15px] hover:bg-[#e6e8fd] transition-colors shadow-sm">Apply URL</button>
                                    </div>
                                )}
                            </div>

                            <div className="flex items-center gap-3 mb-6">
                                <Icon name="Headphones" size={24} className="text-[#1E293B]" />
                                <span className="font-extrabold text-[#1E293B] text-[18px]">Ambient Sound</span>
                            </div>
                            
                            <div className="flex gap-2 justify-between mb-8">
                                {[
                                    { id: 'rain', icon: 'CloudRain', color: 'bg-[#6B63ED] text-white shadow-md', inactive: 'bg-white text-slate-600' },
                                    { id: 'coffee', icon: 'Coffee', color: 'bg-[#6B63ED] text-white shadow-md', inactive: 'bg-white text-slate-600' },
                                    { id: 'waves', icon: 'Waves', color: 'bg-[#6B63ED] text-white shadow-md', inactive: 'bg-white text-slate-600' },
                                    { id: 'forest', icon: 'TreePine', color: 'bg-[#6B63ED] text-white shadow-md', inactive: 'bg-white text-slate-600' },
                                    { id: 'noise', icon: 'Disc', color: 'bg-[#6B63ED] text-white shadow-md', inactive: 'bg-white text-slate-600' }
                                ].map(s => (
                                    <button key={s.id} onClick={() => toggleSound(s.id)}
                                        className={`w-[52px] h-[52px] rounded-full flex items-center justify-center border border-slate-100 transition-all ${activeSound === s.id ? s.color : s.inactive + ' hover:bg-slate-50'}`}>
                                        <Icon name={s.icon} size={22} className={activeSound === s.id ? 'fill-white text-white' : ''} />
                                    </button>
                                ))}
                            </div>
                            
                            <div className="flex items-center gap-4 mb-12 px-2">
                                <Icon name="VolumeX" size={16} className="text-slate-500" />
                                <div className="flex-1 relative flex items-center">
                                    <input type="range" min="0" max="100" value={volume} onChange={(e) => setVolume(Number(e.target.value))} 
                                    className="w-full h-1.5 bg-slate-200 rounded-full appearance-none cursor-pointer relative z-20 outline-none" 
                                    style={{ background: `linear-gradient(to right, #6B63ED ${volume}%, #E2E8F0 ${volume}%)` }}/>
                                    <style>{`
                                        input[type=range]::-webkit-slider-thumb {
                                            -webkit-appearance: none; appearance: none; width: 16px; height: 16px; border-radius: 50%; background: white; border: 2px solid #6B63ED; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                        }
                                    `}</style>
                                </div>
                                <Icon name="Volume2" size={16} className="text-slate-500" />
                            </div>

                            <div className="mt-auto">
                                 <p className="text-[13px] font-bold text-slate-500 uppercase tracking-[0.1em] mb-4">MỤC TIÊU HIỆN TẠI</p>
                                 <div className="bg-[#6B63ED] rounded-[24px] p-7 text-white shadow-[0_12px_30px_-5px_rgba(107,99,237,0.4)] relative overflow-hidden">
                                     <Icon name="Pin" size={20} className="absolute top-6 right-6 text-white/50 fill-current" />
                                     <p className="text-[13px] text-white/80 mb-2 font-medium">CURRENT TASK</p>
                                     <h4 className="font-bold text-[19px] leading-snug w-5/6 pr-4">Hoàn thiện Prototype UI cho Smart Focus Dashboard</h4>
                                     <div className="flex items-center gap-3 mt-8">
                                         <div className="w-5 h-5 rounded-full border-[1.5px] border-white/60 flex items-center justify-center">
                                             <Icon name="Check" size={12} strokeWidth={3} className="text-white" />
                                         </div>
                                         <span className="text-[14px] text-white/90 font-medium">Progress: 65%</span>
                                     </div>
                                 </div>
                            </div>
                        </div>

                    </div>
                </div>
            );
        }"""

    # Do replacements using regex
    # Replace AudioEngine
    content = re.sub(
        r'// ===== Web Audio API Ambient Sound Generator =====.*?const AudioEngine = \(\(\) => \{.*?\n        \}\);\n        \}\)\(\);',
        audio_engine_replacement,
        content,
        flags=re.DOTALL
    )

    # Replace App function entirely
    content = re.sub(
        r'function App\(\) \{.*?\n        \}',
        app_replacement,
        content,
        flags=re.DOTALL
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
