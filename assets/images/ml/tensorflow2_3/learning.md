# 기존 learning 함수

def learing(): 
        """
        MAchine Learning, Tensorflow 
        """
        # Tensorflow Linear Regression
        import tensorflow as tf
        tf.set_random_seed(777)  # for reproducibility
        
        t_a = int(t_aSpbox.get())
        t_t = int(t_tSpbox.get()) + 1
        t_r = float(t_rSpbox.get())
            
        # X and Y data from 0km to 30km
        x_train = [ i/10 for i in xData[0:7]]
        y_train = record_list[t_a-1][0:7]
        
        # Try to find values for W and b to compute y_data = x_data * W + b
        W = tf.Variable(tf.random_normal([1]), name="weight")
        b = tf.Variable(tf.random_normal([1]), name="bias")
        
        # placeholders for a tensor that will be always fed using feed_dict
        # See http://stackoverflow.com/questions/36693740/
        X = tf.placeholder(tf.float32, shape=[None])
        Y = tf.placeholder(tf.float32, shape=[None])
        
        # Our hypothesis XW+b
        hypothesis = X * W + b
        
        # cost/loss function
        cost = tf.reduce_mean(tf.square(hypothesis - Y))
        
        # optimizer
        train = tf.train.GradientDescentOptimizer(learning_rate=t_r).minimize(cost)
        
        # Launch the graph in a session.
        with tf.Session() as sess:
            # Initializes global variables 
            sess.run(tf.global_variables_initializer())
        
            # Fit the line
            log_ScrolledText.insert(END, "%10s %4i %10s %6i %20s %10.8f" % ('\nRunner #', t_a, ', No. of train is', (t_t-1), ', learing rate is ', t_r)+'\n', 'TITLE')
            log_ScrolledText.insert(END, '\n\nCost Decent\n\n','HEADER')
            log_ScrolledText.insert(END, "%20s %20s %20s %20s" % ('Step', 'Cost', 'W', 'b')+'\n\n')
            for step in range(t_t):
                _, cost_val, W_val, b_val = sess.run([train, cost, W, b], feed_dict={X: x_train, Y: y_train})
        
                if step % 100 == 0:
                    # print(step, cost_val, W_val, b_val) 
                    g_xdata.append(step)
                    g_ydata.append(cost_val)
                    log_ScrolledText.insert(END, "%20i %20.5f %20.5f %20.5f" % (step, cost_val, W_val, b_val)+'\n')
            #gn.set_data(g_xdata, g_ydata)
            grad_ax.plot(g_xdata, g_ydata, 'ro')
            grad_ax.set_title('The minimum cost is '+str(cost_val)+' at '+str(step)+'times')
            grad_fig.canvas.draw()    
            
            # Testing our model
            log_ScrolledText.insert(END, "%20s" % ('\n\nHypothesis = X * W + b\n\n'), 'HEADER')
            draw_hypothesis(W_val, b_val)
            log_ScrolledText.insert(END, "%20s" % ('\n\nRecords Prediction\n\n'), 'HEADER')
            log_ScrolledText.insert(END, "%20s %20s %20s %20s" % ('Distance(km)', 'Real record', 'ML Prediction', 'Variation(Second)')+'\n\n')
            for index in range(7, 10):
                x_value = xData[index] / 10
                p_xdata.append(xData[index])
                time = sess.run(hypothesis, feed_dict={X: [x_value]})
                p_ydata.append(time[0])
                log_ScrolledText.insert(END, "%20.3f %20s %20s %20i" % (xData[index], seconds_to_hhmmss(t_ydata[index]), seconds_to_hhmmss(time[0]), (t_ydata[index] - time[0]))+'\n')
    
            dn.set_data(t_xdata, t_ydata)  
            pn.set_data(p_xdata, p_ydata)
            fig.canvas.draw()