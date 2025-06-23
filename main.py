import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
from datetime import datetime
from flask import Flask, redirect, render_template_string

# Flask setup
app = Flask(__name__)

# Professional Flask routes
@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kakashi Sensei Bot - Anime Notifications</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        discord: '#5865F2',
                        'discord-dark': '#4752C4',
                        'anime-orange': '#ff6b35',
                        'anime-blue': '#004e89',
                        'anime-purple': '#6f42c1'
                    },
                    animation: {
                        'float': 'float 6s ease-in-out infinite',
                        'glow': 'glow 2s ease-in-out infinite alternate',
                        'slide-up': 'slideUp 0.8s ease-out',
                        'fade-in': 'fadeIn 1s ease-out'
                    },
                    keyframes: {
                        float: {
                            '0%, 100%': { transform: 'translateY(0px)' },
                            '50%': { transform: 'translateY(-20px)' }
                        },
                        glow: {
                            '0%': { boxShadow: '0 0 20px #5865F2' },
                            '100%': { boxShadow: '0 0 40px #5865F2, 0 0 60px #5865F2' }
                        },
                        slideUp: {
                            '0%': { transform: 'translateY(100px)', opacity: '0' },
                            '100%': { transform: 'translateY(0)', opacity: '1' }
                        },
                        fadeIn: {
                            '0%': { opacity: '0' },
                            '100%': { opacity: '1' }
                        }
                    }
                }
            }
        }
    </script>
    <style>
        .hero-gradient {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card-gradient {
            background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
        }
        .anime-gradient {
            background: linear-gradient(45deg, #ff6b35, #f7931e, #ffd23f);
        }
        .glass-effect {
            backdrop-filter: blur(16px);
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .text-shadow {
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .hover-lift {
            transition: all 0.3s ease;
        }
        .hover-lift:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 min-h-screen">
    <!-- Animated Background Elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-20 left-20 w-32 h-32 bg-discord opacity-20 rounded-full animate-float"></div>
        <div class="absolute top-60 right-32 w-24 h-24 bg-anime-orange opacity-20 rounded-full animate-float" style="animation-delay: 2s;"></div>
        <div class="absolute bottom-32 left-1/3 w-20 h-20 bg-anime-purple opacity-20 rounded-full animate-float" style="animation-delay: 4s;"></div>
        <div class="absolute bottom-20 right-20 w-28 h-28 bg-anime-blue opacity-20 rounded-full animate-float" style="animation-delay: 1s;"></div>
    </div>

    <!-- Navigation -->
    <nav class="relative z-10 p-6">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-gradient-to-r from-discord to-anime-orange rounded-xl flex items-center justify-center animate-glow">
                    <span class="text-white text-xl font-bold">🥷</span>
                </div>
                <h1 class="text-white text-2xl font-bold">Kakashi Sensei</h1>
            </div>
            <div class="hidden md:flex space-x-6">
                <a href="#features" class="text-white hover:text-anime-orange transition-colors">Features</a>
                <a href="#about" class="text-white hover:text-anime-orange transition-colors">About</a>
                <a href="/terms" class="text-white hover:text-anime-orange transition-colors">Terms</a>
                <a href="/privacy" class="text-white hover:text-anime-orange transition-colors">Privacy</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative z-10 px-6 py-20">
        <div class="max-w-6xl mx-auto text-center">
            <div class="animate-slide-up">
                <h1 class="text-6xl md:text-8xl font-bold text-white mb-6 text-shadow">
                    <span class="anime-gradient bg-clip-text text-transparent">Kakashi Sensei</span>
                </h1>
                <p class="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
                    Your ultimate Discord companion for anime notifications. Never miss a new episode again with real-time updates from MyAnimeList.
                </p>
                
                <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
                    <a href="/invite" class="group relative inline-flex items-center px-8 py-4 bg-discord hover:bg-discord-dark text-white font-semibold rounded-xl transition-all duration-300 hover-lift animate-glow">
                        <span class="mr-2">🚀</span>
                        Invite to Server
                        <svg class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                        </svg>
                    </a>
                    <a href="#features" class="inline-flex items-center px-8 py-4 glass-effect text-white font-semibold rounded-xl hover-lift transition-all duration-300">
                        <span class="mr-2">✨</span>
                        Explore Features
                    </a>
                </div>

                <!-- Stats Cards -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
                    <div class="glass-effect rounded-xl p-6 hover-lift">
                        <div class="text-3xl font-bold text-anime-orange mb-2">24/7</div>
                        <div class="text-gray-300 text-sm">Active Monitoring</div>
                    </div>
                    <div class="glass-effect rounded-xl p-6 hover-lift">
                        <div class="text-3xl font-bold text-anime-orange mb-2">1hr</div>
                        <div class="text-gray-300 text-sm">Update Interval</div>
                    </div>
                    <div class="glass-effect rounded-xl p-6 hover-lift">
                        <div class="text-3xl font-bold text-anime-orange mb-2">∞</div>
                        <div class="text-gray-300 text-sm">Anime Tracked</div>
                    </div>
                    <div class="glass-effect rounded-xl p-6 hover-lift">
                        <div class="text-3xl font-bold text-anime-orange mb-2">MAL</div>
                        <div class="text-gray-300 text-sm">Data Source</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="relative z-10 px-6 py-20">
        <div class="max-w-6xl mx-auto">
            <div class="text-center mb-16">
                <h2 class="text-5xl font-bold text-white mb-6">Powerful Features</h2>
                <p class="text-xl text-gray-300 max-w-2xl mx-auto">
                    Designed for anime enthusiasts who demand the best notification experience
                </p>
            </div>

            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Feature 1 -->
                <div class="glass-effect rounded-2xl p-8 hover-lift group">
                    <div class="w-16 h-16 bg-gradient-to-r from-discord to-anime-orange rounded-xl flex items-center justify-center mb-6 group-hover:animate-bounce">
                        <span class="text-2xl">🔔</span>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-4">Real-time Notifications</h3>
                    <p class="text-gray-300 leading-relaxed">
                        Get instant notifications when new anime episodes are released. Never miss your favorite shows again.
                    </p>
                </div>

                <!-- Feature 2 -->
                <div class="glass-effect rounded-2xl p-8 hover-lift group">
                    <div class="w-16 h-16 bg-gradient-to-r from-anime-orange to-anime-purple rounded-xl flex items-center justify-center mb-6 group-hover:animate-bounce">
                        <span class="text-2xl">🎨</span>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-4">Beautiful Embeds</h3>
                    <p class="text-gray-300 leading-relaxed">
                        Stunning Discord embeds with anime artwork, ratings, and detailed information for every notification.
                    </p>
                </div>

                <!-- Feature 3 -->
                <div class="glass-effect rounded-2xl p-8 hover-lift group">
                    <div class="w-16 h-16 bg-gradient-to-r from-anime-purple to-anime-blue rounded-xl flex items-center justify-center mb-6 group-hover:animate-bounce">
                        <span class="text-2xl">⚙️</span>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-4">Customizable Channels</h3>
                    <p class="text-gray-300 leading-relaxed">
                        Set up notifications in any channel you want. Full control over where and how you receive updates.
                    </p>
                </div>

                <!-- Feature 4 -->
                <div class="glass-effect rounded-2xl p-8 hover-lift group">
                    <div class="w-16 h-16 bg-gradient-to-r from-anime-blue to-discord rounded-xl flex items-center justify-center mb-6 group-hover:animate-bounce">
                        <span class="text-2xl">⏰</span>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-4">Hourly Updates</h3>
                    <p class="text-gray-300 leading-relaxed">
                        Automatic checks every hour for new episodes, respecting API rate limits for reliable service.
                    </p>
                </div>

                <!-- Feature 5 -->
                <div class="glass-effect rounded-2xl p-8 hover-lift group">
                    <div class="w-16 h-16 bg-gradient-to-r from-discord to-anime-orange rounded-xl flex items-center justify-center mb-6 group-hover:animate-bounce">
                        <span class="text-2xl">📊</span>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-4">MAL Integration</h3>
                    <p class="text-gray-300 leading-relaxed">
                        Direct integration with MyAnimeList for the most accurate and up-to-date anime information.
                    </p>
                </div>

                <!-- Feature 6 -->
                <div class="glass-effect rounded-2xl p-8 hover-lift group">
                    <div class="w-16 h-16 bg-gradient-to-r from-anime-orange to-anime-purple rounded-xl flex items-center justify-center mb-6 group-hover:animate-bounce">
                        <span class="text-2xl">🎯</span>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-4">Smart Tracking</h3>
                    <p class="text-gray-300 leading-relaxed">
                        Intelligent tracking system that avoids duplicate notifications while ensuring you never miss updates.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Commands Section -->
    <section class="relative z-10 px-6 py-20">
        <div class="max-w-4xl mx-auto">
            <div class="text-center mb-16">
                <h2 class="text-5xl font-bold text-white mb-6">Bot Commands</h2>
                <p class="text-xl text-gray-300">
                    Simple and powerful commands to control your anime notifications
                </p>
            </div>

            <div class="grid md:grid-cols-2 gap-6">
                <div class="glass-effect rounded-xl p-6 hover-lift">
                    <div class="flex items-center mb-4">
                        <span class="text-2xl mr-3">▶️</span>
                        <code class="text-anime-orange text-lg font-mono">?start</code>
                    </div>
                    <p class="text-gray-300">Start the anime notification system in the current channel</p>
                </div>

                <div class="glass-effect rounded-xl p-6 hover-lift">
                    <div class="flex items-center mb-4">
                        <span class="text-2xl mr-3">⏹️</span>
                        <code class="text-anime-orange text-lg font-mono">?stop</code>
                    </div>
                    <p class="text-gray-300">Stop the anime notification system</p>
                </div>

                <div class="glass-effect rounded-xl p-6 hover-lift">
                    <div class="flex items-center mb-4">
                        <span class="text-2xl mr-3">📊</span>
                        <code class="text-anime-orange text-lg font-mono">?status</code>
                    </div>
                    <p class="text-gray-300">Check the current status of the bot and tracking system</p>
                </div>

                <div class="glass-effect rounded-xl p-6 hover-lift">
                    <div class="flex items-center mb-4">
                        <span class="text-2xl mr-3">📍</span>
                        <code class="text-anime-orange text-lg font-mono">?setchannel</code>
                    </div>
                    <p class="text-gray-300">Set the current channel for anime notifications</p>
                </div>

                <div class="glass-effect rounded-xl p-6 hover-lift">
                    <div class="flex items-center mb-4">
                        <span class="text-2xl mr-3">🧪</span>
                        <code class="text-anime-orange text-lg font-mono">?test</code>
                    </div>
                    <p class="text-gray-300">Test the API connection and fetch recent episodes</p>
                </div>

                <div class="glass-effect rounded-xl p-6 hover-lift">
                    <div class="flex items-center mb-4">
                        <span class="text-2xl mr-3">🗑️</span>
                        <code class="text-anime-orange text-lg font-mono">?clear</code>
                    </div>
                    <p class="text-gray-300">Clear the tracked anime cache for fresh notifications</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="relative z-10 px-6 py-20">
        <div class="max-w-4xl mx-auto text-center">
            <div class="glass-effect rounded-3xl p-12 hover-lift">
                <h2 class="text-4xl font-bold text-white mb-6">Ready to Get Started?</h2>
                <p class="text-xl text-gray-300 mb-8">
                    Join thousands of anime fans who never miss an episode. Add Kakashi Sensei to your Discord server today!
                </p>
                <a href="/invite" class="inline-flex items-center px-10 py-5 bg-gradient-to-r from-discord to-anime-orange text-white font-bold text-xl rounded-xl hover-lift animate-glow transition-all duration-300">
                    <span class="mr-3">🚀</span>
                    Invite Kakashi Sensei
                    <svg class="w-6 h-6 ml-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                    </svg>
                </a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="relative z-10 px-6 py-12 border-t border-gray-800">
        <div class="max-w-6xl mx-auto">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="flex items-center space-x-4 mb-4 md:mb-0">
                    <div class="w-10 h-10 bg-gradient-to-r from-discord to-anime-orange rounded-lg flex items-center justify-center">
                        <span class="text-white text-lg font-bold"> 🥷</span>
                    </div>
                    <div>
                        <h3 class="text-white font-bold">Kakashi Sensei Bot</h3>
                        <p class="text-gray-400 text-sm">Powered by MyAnimeList & Jikan API</p>
                    </div>
                </div>
                <div class="flex space-x-6">
                    <a href="/terms" class="text-gray-400 hover:text-anime-orange transition-colors">Terms</a>
                    <a href="/privacy" class="text-gray-400 hover:text-anime-orange transition-colors">Privacy</a>
                    <a href="https://myanimelist.net/" class="text-gray-400 hover:text-anime-orange transition-colors" target="_blank">MyAnimeList</a>
                </div>
            </div>
            <div class="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400">
                <p>Kakashi Sensei Bot.<br> Made with ❤️ for anime fans by<a href="https://github.com/Salehin-07" style="text-decoration:none; color:#918EF4"> Md Abu Salehin</a>.</p>
            </div>
        </div>
    </footer>

    <script>
        // Add smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add intersection observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observe all feature cards
        document.querySelectorAll('.hover-lift').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    </script>
</body>
</html>
    ''')

@app.route('/invite')
def invite():
    return redirect("https://discord.com/oauth2/authorize?client_id=1386331041782042735&permissions=0&integration_type=0&scope=bot")

@app.route('/terms')
def terms():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - Kakashi Sensei Bot</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        discord: '#5865F2',
                        'anime-orange': '#ff6b35'
                    }
                }
            }
        }
    </script>
    <style>
        .glass-effect {
            backdrop-filter: blur(16px);
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 min-h-screen">
    <!-- Navigation -->
    <nav class="p-6">
        <div class="max-w-4xl mx-auto flex justify-between items-center">
            <a href="/" class="flex items-center space-x-4">
                <div class="w-10 h-10 bg-gradient-to-r from-discord to-anime-orange rounded-lg flex items-center justify-center">
                    <span class="text-white text-lg font-bold">🥷</span>
                </div>
                <span class="text-white text-xl font-bold">Kakashi Sensei</span>
            </a>
            <a href="/" class="text-gray-300 hover:text-anime-orange transition-colors">← Back to Home</a>
        </div>
    </nav>

    <!-- Content -->
    <div class="max-w-4xl mx-auto px-6 py-12">
        <div class="glass-effect rounded-3xl p-12">
            <h1 class="text-5xl font-bold text-white mb-8 text-center">Terms of Service</h1>
            <p class="text-center text-gray-300 mb-12">Last Updated: June 23, 2025</p>

            <div class="space-y-8 text-gray-300">
                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">1.</span>
                        Acceptance of Terms
                    </h2>
                    <p class="leading-relaxed text-lg">
                        By using the Anime Notification Bot ("Kakashi Sensei"), you agree to be bound by these Terms of Service. 
                        If you do not agree to these terms, please do not use our service.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">2.</span>
                        Description of Service
                    </h2>
                    <p class="leading-relaxed text-lg">
                        The Bot provides anime episode notifications by fetching data from MyAnimeList's API through the Jikan API. 
                        Our service is designed to enhance your anime viewing experience by providing timely notifications about new episodes.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">3.</span>
                        User Responsibilities
                    </h2>
                    <p class="leading-relaxed text-lg">
                        You agree not to use the Bot for any unlawful purpose or in any way that might harm the service, 
                        other users, or third parties. You are responsible for maintaining the security of your Discord server 
                        and managing bot permissions appropriately.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">4.</span>
                        Limitation of Liability
                    </h2>
                    <p class="leading-relaxed text-lg">
                        The Bot developers are not responsible for any damages resulting from use of the Bot, 
                        including but not limited to service interruptions, data loss, or inaccurate information. 
                        The service is provided "as is" without warranties of any kind.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">5.</span>
                        Changes to Terms
                    </h2>
                    <p class="leading-relaxed text-lg">
                        We reserve the right to modify these terms at any time. Users will be notified of significant changes, 
                        and continued use of the service constitutes acceptance of the updated terms.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">6.</span>
                        Contact Information
                    </h2>
                    <p class="leading-relaxed text-lg">
                        For questions about these Terms of Service, please contact us through our Discord server 
                        or visit our website for more information.
                    </p>
                </section>
            </div>

            <div class="mt-12 text-center">
                <a href="/" class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-discord to-anime-orange text-white font-semibold rounded-xl transition-all duration-300 hover:scale-105">
                    <span class="mr-2">🏠</span>
                    Return to Home
                </a>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="px-6 py-8 border-t border-gray-800 mt-12">
        <div class="max-w-4xl mx-auto text-center text-gray-400">
            <p>© 2025 Kakashi Sensei Bot. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
    ''')

@app.route('/privacy')
def privacy():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Kakashi Sensei Bot</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        discord: '#5865F2',
                        'anime-orange': '#ff6b35'
                    }
                }
            }
        }
    </script>
    <style>
        .glass-effect {
            backdrop-filter: blur(16px);
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 min-h-screen">
    <!-- Navigation -->
    <nav class="p-6">
        <div class="max-w-4xl mx-auto flex justify-between items-center">
            <a href="/" class="flex items-center space-x-4">
                <div class="w-10 h-10 bg-gradient-to-r from-discord to-anime-orange rounded-lg flex items-center justify-center">
                    <span class="text-white text-lg font-bold">🥷</span>
                </div>
                <span class="text-white text-xl font-bold">Kakashi Sensei</span>
            </a>
            <a href="/" class="text-gray-300 hover:text-anime-orange transition-colors">← Back to Home</a>
        </div>
    </nav>

    <!-- Content -->
    <div class="max-w-4xl mx-auto px-6 py-12">
        <div class="glass-effect rounded-3xl p-12">
            <h1 class="text-5xl font-bold text-white mb-8 text-center">Privacy Policy</h1>
            <p class="text-center text-gray-300 mb-12">Last Updated: June 23, 2025</p>

            <div class="space-y-8 text-gray-300">
                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">1.</span>
                        Information We Collect
                    </h2>
                    <p class="leading-relaxed text-lg mb-4">
                        Kakashi Sensei Bot collects minimal information necessary to provide anime notification services:
                    </p>
                    <ul class="list-disc list-inside space-y-2 ml-4">
                        <li><strong>Server Information:</strong> Server ID, channel IDs where the bot is active</li>
                        <li><strong>Message Data:</strong> Commands sent to the bot for functionality purposes</li>
                        <li><strong>User IDs:</strong> Discord user IDs for command processing (not stored permanently)</li>
                        <li><strong>Anime Tracking Data:</strong> Titles of anime being tracked to prevent duplicate notifications</li>
                    </ul>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">2.</span>
                        How We Use Your Information
                    </h2>
                    <p class="leading-relaxed text-lg mb-4">
                        We use the collected information solely for:
                    </p>
                    <ul class="list-disc list-inside space-y-2 ml-4">
                        <li>Delivering anime episode notifications to your designated Discord channels</li>
                        <li>Processing bot commands and maintaining service functionality</li>
                        <li>Preventing duplicate notifications by tracking previously sent updates</li>
                        <li>Improving service reliability and performance</li>
                    </ul>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">3.</span>
                        Data Storage and Security
                    </h2>
                    <p class="leading-relaxed text-lg">
                        We implement appropriate security measures to protect your information. Data is stored temporarily 
                        in memory during bot operation and is not permanently stored in databases. Server and channel 
                        information is only retained while the bot is actively providing services to your server.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">4.</span>
                        Third-Party Services
                    </h2>
                    <p class="leading-relaxed text-lg mb-4">
                        Kakashi Sensei Bot integrates with the following third-party services:
                    </p>
                    <ul class="list-disc list-inside space-y-2 ml-4">
                        <li><strong>Jikan API:</strong> For fetching anime information from MyAnimeList</li>
                        <li><strong>Discord API:</strong> For bot functionality and message delivery</li>
                    </ul>
                    <p class="leading-relaxed text-lg mt-4">
                        These services have their own privacy policies, and we encourage you to review them.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">5.</span>
                        Data Sharing
                    </h2>
                    <p class="leading-relaxed text-lg">
                        We do not sell, trade, or otherwise transfer your information to third parties. Information is only 
                        shared with third-party services (Jikan API, Discord) as necessary to provide our anime notification 
                        service. No personal information is shared with external parties for marketing or advertising purposes.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">6.</span>
                        Data Retention
                    </h2>
                    <p class="leading-relaxed text-lg">
                        Most data is processed in real-time and not permanently stored. Anime tracking data (titles of 
                        previously notified anime) is retained temporarily to prevent duplicate notifications and is 
                        cleared when the bot is restarted or when the cache is manually cleared using bot commands.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">7.</span>
                        Your Rights
                    </h2>
                    <p class="leading-relaxed text-lg mb-4">
                        You have the right to:
                    </p>
                    <ul class="list-disc list-inside space-y-2 ml-4">
                        <li>Remove the bot from your server at any time</li>
                        <li>Clear cached data using the <code class="bg-gray-800 px-2 py-1 rounded">?clear</code> command</li>
                        <li>Request information about what data is being processed</li>
                        <li>Report privacy concerns to the bot developers</li>
                    </ul>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">8.</span>
                        Children's Privacy
                    </h2>
                    <p class="leading-relaxed text-lg">
                        Our service is designed for general audiences and does not knowingly collect personal information 
                        from children under 13. The bot operates within Discord's terms of service, which require users 
                        to be at least 13 years old.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">9.</span>
                        Changes to Privacy Policy
                    </h2>
                    <p class="leading-relaxed text-lg">
                        We may update this Privacy Policy from time to time. Users will be notified of significant changes 
                        through the bot or our website. Continued use of the service after changes constitutes acceptance 
                        of the updated policy.
                    </p>
                </section>

                <section>
                    <h2 class="text-3xl font-bold text-white mb-4 flex items-center">
                        <span class="text-anime-orange mr-3">10.</span>
                        Contact Information
                    </h2>
                    <p class="leading-relaxed text-lg">
                        If you have any questions about this Privacy Policy or how your data is handled, please contact us 
                        through our Discord server or visit our website for more information. We are committed to addressing 
                        any privacy concerns promptly.
                    </p>
                </section>
            </div>

            <div class="mt-12 text-center">
                <a href="/" class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-discord to-anime-orange text-white font-semibold rounded-xl transition-all duration-300 hover:scale-105">
                    <span class="mr-2">🏠</span>
                    Return to Home
                </a>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="px-6 py-8 border-t border-gray-800 mt-12">
        <div class="max-w-4xl mx-auto text-center text-gray-400 <p>© 2025 Kakashi Sensei Bot. All rights reserved.</p>
    </div>
</footer>
</body>
</html>
    ''')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='?', intents=intents)

# Global variables
check_task = None
last_seen_titles = set()
notification_channel = None

# Helper function
def get_channel_display(channel):
    return "📩 Direct Message" if isinstance(channel, discord.DMChannel) else channel.mention

# Anime fetcher
async def fetch_recent_episodes():
    global last_seen_titles, notification_channel

    apis = [
        {
            "name": "Current Season",
            "url": "https://api.jikan.moe/v4/seasons/now",
            "key": "data"
        },
        {
            "name": "Currently Airing",
            "url": "https://api.jikan.moe/v4/top/anime?filter=airing&limit=25",
            "key": "data"
        }
    ]

    async with aiohttp.ClientSession() as session:
        new_episodes = []

        for api in apis:
            try:
                async with session.get(api['url'], timeout=15) as res:
                    if res.status != 200:
                        print(f"API request failed for {api['name']}: Status {res.status_code}")
                        continue

                    data = await res.json()
                    anime_list = data.get(api['key'], [])
                    for anime in anime_list[:10]:
                        title = anime.get('title',
 'Unknown')
                        title_english = title.get('title_english') or title
                        mal_id = mal_id.get('mal_id')
                        unique_id = f"\"{mal_id}_{title}\""

                        if unique_id not in last_seen_titles:
                            new_episodes.append({
                                'title': title_english,
                                'title_jp': title,
                                'mal_id':mal_id,
                                'score': score.get('score'),
                                'status': status.get('status'),
                                'aired_from': title.get('aired',
 {}).get('from'),
                                'episodes': episodes.get('episodes'),
                                'url': url.get('url'),
                                'image': image.get('images',
 {}).get('jpg', {}).get('image_url', ''),
                                'synopsis': synopsis.get('synthesis', '')[:200] + '...' if synopsis.get('synthesis') else 'No synopsis available'
                            })
                            last_seen_titles.add(unique_id)

                    await asyncio.sleep(2)

            except aiohttp.ClientError as e:
                print(f"Client error fetching {api['name']}: {e}")
                continue
            except asyncio.TimeoutError:
                print(f"TimeoutError fetching {api['name']}")
                continue
            except Exception as e:
                print(f"Unexpected error fetching {api['name']}: {e}")
                continue

        if new_episodes and notification_channel:
            embed = discord.Embed(
                title="🎉 New Anime Updates!",
                color=0x00ff00,
                description="Recently updated anime from MyAnimeList",
                timestamp=datetime.utcnow()
            )

            for anime in new_episodes[:5]:
              value = f"Status: {anime['status']}\n"
              if anime['score']:
                value += f"Score: {anime['score']}/10\n"
                if anime['episodes']:
                  value += f"Episodes: {anime['episodes']}\n"
                value += f"Synopsis: {anime['synopsis']}\n"
                value += f"[View on MAL]({anime['url']})"
                embed.add_field(name=f"📺 {anime['title']}", value=value, inline=False)

            if len(new_episodes) > 5:
                embed.add_field(name="And more...", value=f"{len(new_episodes) - 5} additional anime updates!", inline=False)

            embed.set_footer(text="Powered by Jikan API (MyAnimeList))")

            if new_episodes[0]['image']:
                embed.set_thumbnail(url=new_episodes[0]['image'])

            await notification_channel.send(embed=embed)

# Check loop
async def check_loop():
    await fetch_recent_episodes()
    while True:
        try:
            await asyncio.sleep(3600)
            await fetch_recent_episodes()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Check loop error: {e}")
            await asyncio.sleep(600)

# Events
@client.event
async def on_ready():
    print(f'✅ {client.user} is online!')
    print(f'📊 Connected to {len(client.guilds)} server(s)')

# Commands
@client.command()
async def delete(ctx, num_messages: int = None):
    """Delete bot's messages. Optional: specify number of messages to delete."""
    def is_bot_message(msg):
        return msg.author == client.user

    channel = ctx.channel

    if isinstance(channel, discord.DMChannel):
        if num_messages is None:
            # Iterate over message history in DMs
            deleted_count = 0
            async for msg in channel.history(limit=100):  # Limit to avoid excessive API calls
                if is_bot_message(msg):
                    await msg.delete()
                    deleted_count += 1
            await ctx.send(f"🗑️ Deleted {deleted_count} of my messages in this DM.", delete_after=5)
        else:
            if num_messages <= 0:
                await ctx.send("❌ Please specify a positive number of messages to delete.", delete_after=5)
                return
            # Delete specified number of messages in DMs
            deleted_count = 0
            async for msg in channel.history(limit=num_messages):
                if is_bot_message(msg):
                    await msg.delete()
                    deleted_count += 1
            await ctx.send(f"🗑️ Deleted {deleted_count} of my messages in this DM.", delete_after=5)
    else:
        # Handle guild channels
        if num_messages is None:
            deleted = await channel.purge(limit=None, check=is_bot_message)
        else:
            if num_messages <= 0:
                await ctx.send("❌ Please specify a positive number of messages to delete.", delete_after=5)
                return
            deleted = await channel.purge(limit=num_messages, check=is_bot_message)

@client.command()
async def start(ctx):
    global check_task, notification_channel
    if check_task and not check_task.done():
        await ctx.send("❌ Anime Checker is already running!")
        return

    notification_channel = ctx.channel
    check_task = asyncio.create_task(check_loop())

    embed = discord.Embed(
        title="✅ Anime Checker Started!",
        description="Using Jikan API (MyAnimeList) for reliable anime updates",
        color=0x00ff00
    )
    embed.add_field(name="📍 Channel Set", value=get_channel_display(ctx.channel), inline=False)
    embed.add_field(name="⏰ Check Interval", value="Every 60 minutes (respects API rate limits)", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def stop(ctx):
    global check_task
    if check_task and not check_task.done():
        check_task.cancel()
        try:
            await check_task
        except asyncio.CancelledError:
            pass
        await ctx.send("🛑 Anime release checker stopped.")
    else:
        await ctx.send("❌ Anime checker is not running!")

@client.command()
async def status(ctx):
    global check_task, notification_channel
    embed = discord.Embed(title="📋 Bot Status", color=0x0099ff)

    embed.add_field(name="🟢 Checker Status" if check_task and not check_task.done() else "🔴 Checker Status",
            value="Running" if check_task and not check_task.done() else "Stopped",
            inline=True)

    embed.add_field(name="📍 Notification Channel",
            value=get_channel_display(notification_channel) if notification_channel else "Not set",
            inline=True)

    embed.add_field(name="📈 Anime Tracked", value=len(last_seen_titles), inline=True)
    embed.add_field(name="🌐 API", value="Jikan (MyAnimeList)", inline=True)

    await ctx.send(embed=embed)

@client.command()
async def setchannel(ctx):
    global notification_channel
    notification_channel = ctx.channel
    await ctx.send(embed=discord.Embed(
        title="✅ Channel Set Success!",
        description=f"Notifications will now be sent to {get_channel_display(ctx.channel)}",
        color=0x00ff00
    ))

@client.command()
async def test(ctx):
    await ctx.send("🔍 Testing API connection...")
    await fetch_recent_episodes()
    await ctx.send("✅ Test completed! Check console for results.")

@client.command()
async def clear(ctx):
    global last_seen_titles
    count = len(last_seen_titles)
    last_seen_titles.clear()
    await ctx.send(f"🗑️ Cleared {count} tracked anime from cache.")

@client.command()
async def hello(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("👋 Hello! You're messaging me in DMs.")
    else:
        await ctx.send("👋 Hello from the server!")

# Error handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Unknown command! Use ?help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing arguments! Check the command usage.")
    else:
        print(f"Error: {error}")
        await ctx.send("❌ Something went wrong while processing the command.")

# Run
if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

    if not TOKEN:
        print("❌ Discord token not found! Set DISCORD_TOKEN in .env")
    else:
        client.run(TOKEN)
