import graphviz

try:
    dot = graphviz.Digraph(comment='Test')
    dot.node('A', 'Local AI')
    dot.node('B', 'Flowchart')
    dot.edge('A', 'B')
    # This will create a 'test.gv.pdf' in your folder
    dot.render('test-output', view=True) 
    print("Success! Graphviz is working locally.")
except Exception as e:
    print(f"Error: {e}. Check if Graphviz is added to your system PATH.")