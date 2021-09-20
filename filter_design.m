fs = 8192;
a = [0 0 1 1 0 0];

% filter 1
f = [0 640 670 730 760 fs]./fs;
filter1 = firpm(300,f,a);
save('filter1.mat','filter1')

% filter 2
f = [0 700 735 805 840 fs]./fs;
filter2 = firpm(300,f,a);
save('filter2.mat','filter2')

% filter 3
f = [0 800 825 875 900 fs]./fs;
filter3 = firpm(300,f,a);
save('filter3.mat','filter3')

% filter 4
f = [0 880 910 970 1000 fs]./fs;
filter4 = firpm(300,f,a);
save('filter4.mat','filter4')

% filter 5
f = [0 1150 1190 1230 1270 fs]./fs;
filter5 = firpm(300,f,a);
save('filter5.mat','filter5')

% filter 6
f = [0 1250 1300 1400 1450 fs]./fs;
filter6 = firpm(300,f,a);
save('filter6.mat','filter6')

% filter 7
f = [0 1400 1450 1550 1600 fs]./fs;
filter7 = firpm(300,f,a);
save('filter7.mat','filter7')

% filter 8
f = [0 1550 1600 1700 1750 fs]./fs;
filter8 = firpm(300,f,a);
save('filter8.mat','filter8')


%% plot
f = [0 1100 1150 1250 1300 fs]./fs;
[h,w] = freqz(filter5,1,fs);
plot(f,a,w/pi,abs(h))
legend('Ideal','firpm Design')
xlabel 'Radian Frequency (\omega/\pi)', ylabel 'Magnitude'