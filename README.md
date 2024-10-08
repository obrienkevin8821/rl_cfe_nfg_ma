<h2>A framework for multi-agent algorithmic recourse in normal form games</h2>
<p>This repository holds the code which was used for experimentation and implementation purposes when writing the article <b>"A framework for multi-agent algorithmic recourse in normal form games"</b> - see <b>AlgorithmicRecourse_Paper1.pdf</b>. Please note this is not a published article and is only a draft.</p>
<h3>Note the following:</h3>
<ul>
  <li><b>nfg.ipynb:</b> Notebook demomstrating code used for playing normal form games and developing strategies, best responses, to play these games. Code in this notebook was developed from theory and experiments discussed in AlgorithmicRecourse_Paper1.pdf</li>
  <li><b>server.py</b>: Run this script to start the teaching service.</li>
  <li><b>client.py</b>: Run this script twice to start clients for the teaching service. One client will act as the opponent and the other client will act as the RL agent. The script client.py includes an implementation of algorithm 1 and server.py includes an implemention algorithms 2 and 3 presented in  AlgorithmicRecourse_Paper1.pdf</li>
  <li><b>policy.json</b>: This file is generated from client.py for RL agent to store best responses learnt by RL agent from advise recieved from teaching service.</li>
  <li><b>cfe.log</b>: This file is generated by teaching service (server.py), to store CFE generated which is sent to RL agent client.</li>
  <li><b>comparison.ipynb</b>: Notebook demonstrating using nashpy and ramo for determining best responses and comparing with code demonstrated in nfg.ipynb. Purpose of this was to validate code written in nfg.ipynb.</li>
</ul>
