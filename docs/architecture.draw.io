<mxfile host="app.diagrams.net" modified="2024-05-20T00:00:00.000Z" agent="5.0" version="21.0.0" type="device">
  <diagram id="multi-agent-smart-compose" name="Architecture">
    <mxGraphModel dx="1422" dy="798" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="850" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <mxCell id="state" value="Shared State (SmartComposeState)&#xa;—&#xa;user_input | tone | draft | styled_draft&#xa;feedback_score | is_factually_ok&#xa;review_decision | iteration" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#dae8fc;strokeColor=#6c8ebf;align=center;" vertex="1" parent="1">
          <mxGeometry x="410" y="40" width="280" height="100" as="geometry" />
        </mxCell>

        <mxCell id="input" value="User Input &amp; Tone" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="40" y="240" width="120" height="60" as="geometry" />
        </mxCell>

        <mxCell id="node1" value="Drafting Agent&#xa;(Gemini LLM)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="220" y="240" width="120" height="60" as="geometry" />
        </mxCell>

        <mxCell id="node2" value="Style Agent&#xa;(Tone Mapper)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="380" y="240" width="120" height="60" as="geometry" />
        </mxCell>

        <mxCell id="node3" value="Feedback Agent&#xa;(Scoring Logic)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="540" y="240" width="120" height="60" as="geometry" />
        </mxCell>

        <mxCell id="node4" value="Fact-Checking Agent&#xa;(Wikipedia Tool)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="700" y="240" width="140" height="60" as="geometry" />
        </mxCell>

        <mxCell id="node5" value="Human Review&#xa;Agent" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="880" y="240" width="120" height="60" as="geometry" />
        </mxCell>

        <mxCell id="gemini" value="Google Gemini API" style="ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="210" y="360" width="140" height="80" as="geometry" />
        </mxCell>

        <mxCell id="wiki" value="Wikipedia API" style="ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="700" y="360" width="140" height="80" as="geometry" />
        </mxCell>

        <mxCell id="supervisor" value="Supervisor Router&#xa;(Conditional Edge)" style="rhombus;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
          <mxGeometry x="460" y="480" width="180" height="110" as="geometry" />
        </mxCell>

        <mxCell id="end" value="END" style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;fontColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="720" y="505" width="80" height="60" as="geometry" />
        </mxCell>

        <mxCell id="e1" edge="1" parent="1" source="input" target="node1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e2" edge="1" parent="1" source="node1" target="node2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e3" edge="1" parent="1" source="node2" target="node3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e4" edge="1" parent="1" source="node3" target="node4"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e5" edge="1" parent="1" source="node4" target="node5"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e6" edge="1" parent="1" source="node5" target="supervisor"><mxGeometry relative="1" as="geometry"><mxPoint x="940" y="540" as="targetPoint" /><Array points="940,535" /></mxGeometry></mxCell>
        
        <mxCell id="t1" edge="1" parent="1" source="node1" target="gemini" style="strokeDashArray=1 3;"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="t2" edge="1" parent="1" source="node4" target="wiki" style="strokeDashArray=1 3;"><mxGeometry relative="1" as="geometry" /></mxCell>
        
        <mxCell id="e7" value="Needs Revision / Fail Fact-Check /&#xa;Human Reject &amp; Iteration &lt; 2" edge="1" parent="1" source="supervisor" target="node1">
          <mxGeometry x="-0.8" relative="1" as="geometry"><Array points="280,535" /><mxPoint as="offset" /></mxGeometry>
        </mxCell>
        
        <mxCell id="e8" value="Finish" edge="1" parent="1" source="supervisor" target="end"><mxGeometry relative="1" as="geometry" /></mxCell>

        <mxCell id="s1" edge="1" parent="1" source="node1" target="state" style="strokeColor=#b3b3b3;dashed=1;"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="s2" edge="1" parent="1" source="node5" target="state" style="strokeColor=#b3b3b3;dashed=1;"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>