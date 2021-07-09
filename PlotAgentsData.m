fname = 'Agents_Data.json';
fid = fopen(fname);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
val = jsondecode(str);
clf
subplot(1,2,1)
for i=1:length(val.AgentsList)
hold on
plot(val.Time,val.AgentsList(i).Cash,'DisplayName',['Agent ' num2str(i)])
end
xlabel('Time (game ticks)')
ylabel('Cash')
legend
axis([0 max(val.Time) 0 max(val.AgentsList(i).Cash)*1.1])
grid on

subplot(1,2,2)
for i=1:length(val.AgentsList)
hold on
plot(val.Time,val.AgentsList(i).Store,'DisplayName',['Agent ' num2str(i)])
end
xlabel('Time (game ticks)')
ylabel('Store')
legend
axis([0 max(val.Time) 0 max(val.AgentsList(1).Store)*1.1])
grid on