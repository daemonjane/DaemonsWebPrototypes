<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold mb-6">Contact Us</h1>
    <div class="grid md:grid-cols-2 gap-8">
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h2 class="text-xl font-semibold mb-4">Send a Message</h2>
        <form @submit.prevent>
          <input type="text" placeholder="Name" class="w-full bg-slate-800 p-2 rounded mb-3">
          <input type="email" placeholder="Email" class="w-full bg-slate-800 p-2 rounded mb-3">
          <textarea rows="4" placeholder="Message" class="w-full bg-slate-800 p-2 rounded mb-3"></textarea>
          <button type="submit" class="bg-cyan-600 px-6 py-2 rounded">Send</button>
        </form>
      </div>
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h2 class="text-xl font-semibold mb-4">Info</h2>
        <p>Email: support@techstore.com</p>
        <p>Phone: +1 (555) 789-0123</p>
        <p>Address: 123 Cyber Lane, Silicon Valley, CA</p>
      </div>
    </div>
  </div>
</template>